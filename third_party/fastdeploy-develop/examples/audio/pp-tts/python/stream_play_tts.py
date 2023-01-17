# Copyright (c) 2022 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import math
import os
import time

import fastdeploy as fd
import numpy as np
import soundfile as sf

from paddlespeech.server.utils.util import denorm
from paddlespeech.server.utils.util import get_chunks
from paddlespeech.t2s.frontend.zh_frontend import Frontend

model_name_fastspeech2 = "fastspeech2_cnndecoder_csmsc_streaming_static_1.0.0"
model_zip_fastspeech2 = model_name_fastspeech2 + ".zip"
model_url_fastspeech2 = "https://paddlespeech.bj.bcebos.com/Parakeet/released_models/fastspeech2/" + model_zip_fastspeech2
model_name_mb_melgan = "mb_melgan_csmsc_static_0.1.1"
model_zip_mb_melgan = model_name_mb_melgan + ".zip"
model_url_mb_melgan = "https://paddlespeech.bj.bcebos.com/Parakeet/released_models/mb_melgan/" + model_zip_mb_melgan

dir_name = os.path.dirname(os.path.realpath(__file__)) + "/"

if not os.path.exists(model_name_fastspeech2):
    if os.path.exists(model_zip_fastspeech2):
        os.remove(model_zip_fastspeech2)
    fd.download_and_decompress(model_url_fastspeech2, path=dir_name)
    os.remove(model_zip_fastspeech2)
if not os.path.exists(model_name_mb_melgan):
    if os.path.exists(model_zip_mb_melgan):
        os.remove(model_zip_mb_melgan)
    fd.download_and_decompress(model_url_mb_melgan, path=dir_name)
    os.remove(model_zip_mb_melgan)

voc_block = 36
voc_pad = 14
am_block = 72
am_pad = 12
voc_upsample = 300

# 模型路径

phones_dict = dir_name + model_name_fastspeech2 + "/phone_id_map.txt"
am_stat_path = dir_name + model_name_fastspeech2 + "/speech_stats.npy"

am_encoder_model = dir_name + model_name_fastspeech2 + "/fastspeech2_csmsc_am_encoder_infer.pdmodel"
am_decoder_model = dir_name + model_name_fastspeech2 + "/fastspeech2_csmsc_am_decoder.pdmodel"
am_postnet_model = dir_name + model_name_fastspeech2 + "/fastspeech2_csmsc_am_postnet.pdmodel"
voc_melgan_model = dir_name + model_name_mb_melgan + "/mb_melgan_csmsc.pdmodel"

am_encoder_para = dir_name + model_name_fastspeech2 + "/fastspeech2_csmsc_am_encoder_infer.pdiparams"
am_decoder_para = dir_name + model_name_fastspeech2 + "/fastspeech2_csmsc_am_decoder.pdiparams"
am_postnet_para = dir_name + model_name_fastspeech2 + "/fastspeech2_csmsc_am_postnet.pdiparams"
voc_melgan_para = dir_name + model_name_mb_melgan + "/mb_melgan_csmsc.pdiparams"

frontend = Frontend(phone_vocab_path=phones_dict, tone_vocab_path=None)
am_mu, am_std = np.load(am_stat_path)

option_1 = fd.RuntimeOption()
option_1.set_model_path(am_encoder_model, am_encoder_para)
option_1.use_cpu()
option_1.use_ort_backend()
option_1.set_cpu_thread_num(12)
am_encoder_runtime = fd.Runtime(option_1)

option_2 = fd.RuntimeOption()
option_2.set_model_path(am_decoder_model, am_decoder_para)
option_2.use_cpu()
option_2.use_ort_backend()
option_2.set_cpu_thread_num(12)
am_decoder_runtime = fd.Runtime(option_2)

option_3 = fd.RuntimeOption()
option_3.set_model_path(am_postnet_model, am_postnet_para)
option_3.use_cpu()
option_3.use_ort_backend()
option_3.set_cpu_thread_num(12)
am_postnet_runtime = fd.Runtime(option_3)

option_4 = fd.RuntimeOption()
option_4.set_model_path(voc_melgan_model, voc_melgan_para)
option_4.use_cpu()
option_4.use_ort_backend()
option_4.set_cpu_thread_num(12)
voc_melgan_runtime = fd.Runtime(option_4)


def depadding(data, chunk_num, chunk_id, block, pad, upsample):
    """ 
    Streaming inference removes the result of pad inference
    """
    front_pad = min(chunk_id * block, pad)
    # first chunk
    if chunk_id == 0:
        data = data[:block * upsample]
    # last chunk
    elif chunk_id == chunk_num - 1:
        data = data[front_pad * upsample:]
    # middle chunk
    else:
        data = data[front_pad * upsample:(front_pad + block) * upsample]

    return data


def inference_stream(text):
    input_ids = frontend.get_input_ids(
        text, merge_sentences=False, get_tone_ids=False)
    phone_ids = input_ids["phone_ids"]
    for i in range(len(phone_ids)):
        part_phone_ids = phone_ids[i].numpy()
        voc_chunk_id = 0
        orig_hs = am_encoder_runtime.infer({
            'text':
            part_phone_ids.astype("int64")
        })
        orig_hs = orig_hs[0]

        # streaming voc chunk info
        mel_len = orig_hs.shape[1]
        voc_chunk_num = math.ceil(mel_len / voc_block)
        start = 0
        end = min(voc_block + voc_pad, mel_len)

        # streaming am
        hss = get_chunks(orig_hs, am_block, am_pad, "am")
        am_chunk_num = len(hss)
        for i, hs in enumerate(hss):
            am_decoder_output = am_decoder_runtime.infer({
                'xs':
                hs.astype("float32")
            })

            am_postnet_output = am_postnet_runtime.infer({
                'xs':
                np.transpose(am_decoder_output[0], (0, 2, 1))
            })
            am_output_data = am_decoder_output + np.transpose(
                am_postnet_output[0], (0, 2, 1))
            normalized_mel = am_output_data[0][0]

            sub_mel = denorm(normalized_mel, am_mu, am_std)
            sub_mel = depadding(sub_mel, am_chunk_num, i, am_block, am_pad, 1)

            if i == 0:
                mel_streaming = sub_mel
            else:
                mel_streaming = np.concatenate((mel_streaming, sub_mel), axis=0)

            # streaming voc
            # 当流式AM推理的mel帧数大于流式voc推理的chunk size，开始进行流式voc 推理
            while (mel_streaming.shape[0] >= end and
                   voc_chunk_id < voc_chunk_num):
                voc_chunk = mel_streaming[start:end, :]

                sub_wav = voc_melgan_runtime.infer({
                    'logmel':
                    voc_chunk.astype("float32")
                })
                sub_wav = depadding(sub_wav[0], voc_chunk_num, voc_chunk_id,
                                    voc_block, voc_pad, voc_upsample)

                yield sub_wav

                voc_chunk_id += 1
                start = max(0, voc_chunk_id * voc_block - voc_pad)
                end = min((voc_chunk_id + 1) * voc_block + voc_pad, mel_len)


if __name__ == '__main__':
    text = "欢迎使用飞桨语音合成系统，测试一下合成效果。"
    # warm up
    # onnxruntime 第一次时间会长一些，建议先 warmup 一下
    '''
    # pyaudio 播放
    p = pyaudio.PyAudio()
    stream = p.open(
        format=p.get_format_from_width(2),  # int16
        channels=1,
        rate=24000,
        output=True)
    '''
    # 计时
    wavs = []
    t1 = time.time()
    for sub_wav in inference_stream(text):
        print("响应时间：", time.time() - t1)
        t1 = time.time()
        wavs.append(sub_wav.flatten())
        # float32 to int16
        #wav = float2pcm(sub_wav)
        # to bytes  
        #wav_bytes = wav.tobytes()
        #stream.write(wav_bytes)

    # 关闭 pyaudio 播放器
    #stream.stop_stream()
    #stream.close()
    #p.terminate()

    # 流式合成的结果导出
    wav = np.concatenate(wavs)
    sf.write("demo_stream.wav", data=wav, samplerate=24000)
