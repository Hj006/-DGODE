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

---

## 遇到的问题

1. **Mac 系统遗留文件问题**

   * 在数据集中发现来自 macOS 的隐藏文件（如 `.DS_Store` 等），可能会导致数据读取异常。
   * **解决办法**：加载脚本中加入自动忽略逻辑以及清理

2. **ImageBind 不支持 `.avi` 视频格式**

   * ImageBind 目前无法直接读取 `.avi` 格式的视频文件。
   * **解决办法**：先在本地进行视频格式转换，新增了一个脚本 `avi_to_mp4.py` 用于将 `.avi` 文件转成可被 ImageBind 读取的格式（如 `.mp4`）。

3. **显存不足问题**

   * 使用 24GB 显存的 GPU 无法完整运行 ImageBind - huge 特征提取功能，出现炸显存问题。
   * **可能原因**：模型规模较大，或者代码存在显存释放不及时的情况。
   * **解决办法**：计划更换更大显存的 GPU 进行尝试；同时将检查并优化现有代码以减少显存占用。

   * **2025/10/29**：发现是视频需要切分，否则显存。



4. 数据切分上面遇到问题

暂时定下来希望使用如下的切分：

IEMOCAP/
└── Session1/
    ├── Session1/dialog/avi/DivX/Ses01F_impro01.mp4        ← 整段视频
    ├── Session1/sentences/wav/Ses01F_impro01/             ← 已切好的音频片段
    │      ├── Ses01F_impro01_F000.wav
    │      ├── Ses01F_impro01_F001.wav
    │      ├── ...
    │
    └── Session1/sentences/ForcedAlignment/Ses01F_impro01/ ← 对齐信息（精确到词）
           ├── Ses01F_impro01_F000.wdseg
           ├── Ses01F_impro01_F001.wdseg
           ├── ...


---
---

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


