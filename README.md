# TODO

==Stage 1==: 检索式(单轮对话)、生成式(多轮对话) [2 systems]

==Stage 2==: 检索+生成 [1 system] (检索辅助生成)

--------------------（以上为非任务型对话系统）--------------------

(maybe==)Stage 3==: 任务型对话系统

> **Reference(科普类)**
>
> [1]https://zhuanlan.zhihu.com/p/83825070 (对话系统概述)
>
> [2]https://blog.csdn.net/baidu_41617231/article/details/89187339?spm=1001.2101.3001.6650.5&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-5.topblog&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-5.topblog&utm_relevant_index=10 (多轮对话)
>
> [3]https://zhuanlan.zhihu.com/p/82827048 (多轮对话paper合集)
>
> [4]https://blog.csdn.net/sinat_33761963/article/details/79011160 (对话系统概述)
>
> [5]https://zhuanlan.zhihu.com/p/150119544 (对话系统概述)

## stage 1

|                             Todo                             | 检索式（单轮） |            Todo            | 生成式（多轮） |
| :----------------------------------------------------------: | :------------: | :------------------------: | :------------: |
| 词句向量化/相似度计算方法([传统]tfidf优化：==BM25==)**[2]**  |                |          对话历史          |                |
| **词**向量化方法(==word2vec/GloVe==) +**句**向量化方法(==sif==)**[1]** |                | 加强解码时对关键信息的关注 |                |
|            文本相似度[深度学习]==DSSM==...(?) [3]            |                |  引入额外信息加强对话理解  |                |
|                   （倒排索引、检索召回？）                   |                |                            |                |
|                         🌟**语料库**                          |                |                            |                |
|                           KBQA（？                           |                |                            |                |

> **reference**
>
> [1]https://zhuanlan.zhihu.com/p/111710604 （SIF）
>
> [2]https://zhuanlan.zhihu.com/p/113224707 （BM25）
>
> [3]https://blog.csdn.net/fhzmsj2008Plus/article/details/90210711 (检索式问答系统-深度学习进行语义匹配paper)
>
> [4]https://www.zhihu.com/question/299549788/answer/561907291 (sentence embedding)

## stage 2

TBC...

> **reference**
>
> [1]https://zhuanlan.zhihu.com/p/107755040 (检索生成融合模型paper)

## stage 3

TBC...

