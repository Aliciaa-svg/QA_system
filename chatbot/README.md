# 对话机器人训练实验 - 基于seq2seq及attention机制
   项目是基于官方的[对话机器人教程](https://pytorch.org/tutorials/beginner/chatbot_tutorial.html)进行改写的。可以实现基于原始的对话语料（一问一答形式）训练深度学习对话机器人。  
具体可实现效果如下：    
   ![](examples/chat_record1.png)

## 所需环境
pytorch    
pkuseg  
random
itertools
os
logging
re
tqdm
若有提示有需要额外安装的环境可使用'pip install'命令进行安装，例如：pip install pkuseg

## 项目构成
```
├── corpus    存放语料及语料预处理代码
├── data.py   数据预处理
├── data_transform.py  将数据转化成模型能够接收的格式
├── evaluate.py  测试模型
├── main.py  训练主程序
├── model.py  编码器-解码器模型
├── models   存储模型
├── settings.py  项目参数
├── train.py   训练相关代码
├── utilis.py  工具函数
└── vocabulary.py  将文本字符转化为字典
```
 
## 如何训练模型？
修改setting文件的若干参数， 其他参数都可以不用管， 必须要修改的是以下参数：  
- device: 默认'cpu'；也可以使用GPU，修改为'cuda:0'；注意在训练过程中，根据实际情况可修改device参数，在测试过程中，则需设置为'cpu';
- corpus_name语料名称）， 最后模型的命名会根据这个来；可选qingyun或xiaohuangji
- data_file（数据所在位置），可选： corpus/qingyun_seg或corpus/xhj_seg, 
以青云语料数据为例， 数据形式如下（需要分词）:
```
南京 在 哪里 | 在 这里 了
咋死 ??? 红烧 还是 爆炒 | 哦 了 哦 了 哦 了 , 咱 聊 点 别的 吧
额 麻麻 怎么 会 有 那 玩意儿 | 无法 理解 您 的话 ， 获取 帮助 请 发送 help
孩纸 , 新年 快乐 | {r + }同 乐同乐 ， 大家 一起 乐 ~
```
- 语料的处理的方法名称：read_voc_method， 可选：qingyun或xhj， 两者分别对青语云和小黄鸡语料
- voc_path：训练中加载数据后，对voc进行保存，在测试时可直接进行加载，可选：corpus/voc_qingyun, corpus/voc_xhj
- pairs_path： 训练中加载数据后，对pairs进行保存，在测试时可直接进行加载，可选：corpus/pairs_qingyun, corpus/pairs_xhj
- EvalFile：测试时，保存模型的位置，根据实际情况填写


在配置完其他训练相关参数以后， 可以运行以下代码来训练模型:
```
 python main.py
```
这样就会在models下面出现相应的模型， 然后我们可以通过运行以下代码来测试模型的效果:
```
python evaluate.py
```



   
  
 
