# Dynamic Graph Neural Ordinary Differential Equation

复现论文：
**Dynamic Graph Neural Ordinary Differential Equation Network**
原论文可见：`Dynamic Graph Neural Ordinary Differential Equation Network for.pdf`



## 项目简介

本项目旨在复现论文 *Dynamic Graph Neural Ordinary Differential Equation Network* 的核心方法与实验流程。
特征提取：实验依托 **ImageBind 多模态预训练模型** 进行特征提取。




## 环境与依赖

### 云端环境说明

请参考以下文档以在云端环境中安装依赖：

**云端安装指令文件**：
`云端安装imagebind.txt`

该文件包含在云端服务器中安装 **ImageBind** 模型的详细步骤与命令。


## 数据集与预训练模型

本项目暂时使用的基础数据集为 **IEMOCAP**，
该数据集包含多模态情感识别数据（音频、文本、视频及动作捕捉信息）。

**数据集与ImageBind官方预训练模型下载链接：**

通过百度网盘获取：

```
链接: https://pan.baidu.com/s/1B0DwauBzcMk683m-F6ydeg  
提取码: same
```

> 数据集中包含官方提供的 **pre-trained ImageBind 模型** 文件，可直接用于特征提取。


## 模型结构说明

* 模型主干：Dynamic Graph Neural ODE
* 特征输入：来自 ImageBind 的多模态嵌入（audio/text/vision embedding）
* 任务目标：多模态情感分类 / 时序节点预测


## 使用流程

1. **准备数据集**

   * 下载并解压 IEMOCAP 数据；
   * 将数据放置于 `/ImageBind/datasets/IEMOCAP/` 目录下。

2. **安装依赖**

   参考 `云端安装imagebind.txt`。

3. **提取多模态特征**

   ```bash
   python extract_embeddings.py
   ```

4. **训练 DG-NODE 模型**

   ```bash
   python train_dgnode.py
   ```

5. **评估与可视化**

   ```bash
   python evaluate.py
   ```


## 文件说明

| 文件名                                                                 | 说明                   |
| --------------------------------------------------------------------- | -------------------- |
| `Dynamic Graph Neural Ordinary Differential Equation Network for.pdf` | 原论文                  |
| `云端安装imagebind.txt`                                                | 云端环境下的安装与运行指令        |
| `extract_embeddings.py`                                               | 从 IEMOCAP 数据中提取多模态嵌入 |
| `train_dgnode.py`                                                     | 动态图神经微分方程模型训练脚本      |
| `evaluate.py`                                                         | 模型评估与结果可视化           |
| `README.md`                                                           | 当前说明文档               |


## 联系方式

Email: jiangxiaobai1142&#64;gmail.com

