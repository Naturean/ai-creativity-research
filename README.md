# 毕业设计

主要研究AI辅助下的创造性表现，本仓库为本研究相关代码。

## 目录结构

- `analysis`: 数据分析代码
  - `processing`: 计算指标，产出数据文件
  - `reporting`: 可视化、统计分析，用于最终报告
- `data`: 公共数据
  - `analysis`: 数据分析结果
    - `ai_freq`: AI调用频率、时机分析
    - `post_call`: 调用后行为分析
    - `pre_call`: 调用前认知分析
    - `scoring`: AUT用途评分
  - `pickle`: 二进制数据文件，如AI调用事件、用户回答、AI提示等
  - `processed`: 预处理后的数据
  - `raw`: 原始数据
    - `psychopy`: 实验程序数据
    - `questionnaire`: 问卷数据（主文件）
  - `temp`: 临时文件，一般存储外部评分网站（如CAP）使用时所用的输入文件
  - `to_review`: 审核数据
- `modules`: 外部模块，通常是纯Python模块，会在分析中导入
  - `semantic_toolbox`: 语义距离处理工具
- `preprocess`: 预处理代码
- `review`: 审核代码
- `test`: 测试代码
