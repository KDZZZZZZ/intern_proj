# 话题激发表决算法

## 算法数学公式

### 1. 定义变量

首先，定义算法中涉及的所有变量：

- **大五人格特质（Big Five Personality Traits）**:
  \[
  \begin{aligned}
    O & : \text{开放性（Openness）} \\
    C & : \text{责任感（Conscientiousness）} \\
    E & : \text{外向性（Extraversion）} \\
    A & : \text{宜人性（Agreeableness）} \\
    N & : \text{神经质（Neuroticism）}
  \end{aligned}
  \]

- **情感状态（Mood VAD Tensor）**:
  \[
  \begin{aligned}
    V & : \text{效价（Valence）} \\
    A & : \text{唤醒（Arousal）} \\
    D & : \text{支配（Dominance）}
  \end{aligned}
  \]

- **好感度（Affinity）**:
  \[
  \text{Aff} \in [0, 1]
  \]

- **话题关联度（Topic Relevance）**:
  \[
  T \in [0, 1]
  \]

### 2. 权重定义

为每个主要因素分配权重，反映其在决策中的重要性：

\[
w_p, \ w_m, \ w_a, \ w_t
\]

其中：

\[
\begin{aligned}
w_p & : \text{人格特质的权重} \\
w_m & : \text{情感状态的权重} \\
w_a & : \text{好感度的权重} \\
w_t & : \text{话题关联度的权重}
\end{aligned}
\]

**假设满足权重之和为1**：

\[
w_p + w_m + w_a + w_t = 1
\]

### 3. 人格特质评分（Personality Score）

每个人格特质对话题激发的影响通过对应的权重表示：

\[
p = \sum_{i=1}^{5} w_{p_i} \cdot T_i = w_{O} \cdot O + w_{C} \cdot C + w_{E} \cdot E + w_{A} \cdot A + w_{N} \cdot N
\]

其中 \( w_{p_i} \) 为各人格特质的权重，满足：

\[
\sum_{i=1}^{5} w_{p_i} = 1
\]

### 4. 情感状态评分（Mood Score）

情感状态通过VAD三个维度及其对应权重计算：

\[
m = \sum_{j=1}^{3} w_{m_j} \cdot \text{Mood}_j = w_V \cdot V + w_A \cdot A + w_D \cdot D
\]

其中 \( w_{m_j} \) 为VAD三个维度的权重，满足：

\[
\sum_{j=1}^{3} w_{m_j} = 1
\]

### 5. 综合得分（Composite Score）

将各部分得分按其权重相加，得到一个综合得分：

\[
S = w_p \cdot p + w_m \cdot m + w_a \cdot \text{Aff} + w_t \cdot T
\]

### 6. 阈值判断（Threshold Comparison）

设定一个阈值 \(\theta\)，用于判断是否激发话题：

\[
\text{激发话题} =
\begin{cases}
\text{是}, & \text{如果 } S \geq \theta \\
\text{否}, & \text{否则}
\end{cases}
\]

### 7. 完整公式总结

将上述步骤综合起来，完整的判断是否激发话题的数学公式如下：

\[
\begin{aligned}
p &= w_{O} \cdot O + w_{C} \cdot C + w_{E} \cdot E + w_{A} \cdot A + w_{N} \cdot N \\
m &= w_V \cdot V + w_A \cdot A + w_D \cdot D \\
S &= w_p \cdot p + w_m \cdot m + w_a \cdot \text{Aff} + w_t \cdot T \\
\text{激发话题} &=
\begin{cases}
\text{是}, & \text{如果 } S \geq \theta \\
\text{否}, & \text{否则}
\end{cases}
\end{aligned}
\]

### 8. 具体实例

假设权重如下：

\[
w_p = 0.3, \quad w_m = 0.2, \quad w_a = 0.3, \quad w_t = 0.2
\]

且各人格特质及VAD维度的权重为：

\[
\begin{aligned}
w_{O} &= 0.9, \quad w_{C} = 0.6, \quad w_{E} = 0.7, \quad w_{A} = 0.8, \quad w_{N} = 0.4 \\
w_V &= 0.7, \quad w_A = 0.3, \quad w_D = 0.5
\end{aligned}
\]

给定输入数据：

\[
\begin{aligned}
O &= 0.7, \quad C = 0.6, \quad E = 0.5, \quad A = 0.8, \quad N = 0.3 \\
V &= 0.8, \quad A = 0.5, \quad D = 0.6 \\
\text{Aff} &= 0.75, \quad T = 0.85 \\
\theta &= 0.6
\end{aligned}
\]

计算过程如下：

\[
\begin{aligned}
p &= 0.9 \times 0.7 + 0.6 \times 0.6 + 0.7 \times 0.5 + 0.8 \times 0.8 + 0.4 \times 0.3 \\
&= 0.63 + 0.36 + 0.35 + 0.64 + 0.12 \\
&= 2.10 \\
&\Rightarrow \text{标准化}: \quad p = \frac{2.10 - \text{min}(p)}{\text{max}(p) - \text{min}(p)} = 0.75 \ \text{（例如）} \\
m &= 0.7 \times 0.8 + 0.3 \times 0.5 + 0.5 \times 0.6 \\
&= 0.56 + 0.15 + 0.30 \\
&= 1.01 \\
&\Rightarrow \text{标准化}: \quad m = \frac{1.01 - \text{min}(m)}{\text{max}(m) - \text{min}(m)} = 0.67 \ \text{（例如）} \\
S &= 0.3 \times 0.75 + 0.2 \times 0.67 + 0.3 \times 0.75 + 0.2 \times 0.85 \\
&= 0.225 + 0.134 + 0.225 + 0.170 \\
&= 0.754 \\
\end{aligned}
\]

判断：

\[
0.754 \geq 0.6 \quad \Rightarrow \quad \text{激发话题: 是}
\]

