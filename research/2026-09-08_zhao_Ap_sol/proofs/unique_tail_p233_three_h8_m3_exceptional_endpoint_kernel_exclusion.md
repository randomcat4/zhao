# \(p=233\) 三长八 \(m=3\) 例外曲线轨道的共同端点核排除

STATUS: **PROVED REDUCTION / INDEPENDENT REVIEW CORRECT /
GLOBAL INCOMPLETE**

## 1. 真实五位置共同端点核

在唯一 \(m=3\) 掩码态中，令

\[
A_0=H_1\cap H_2\cap H_3
=\{y_0\}\mathbin{\dot\cup}A_{123}.
\tag{1}
\]

因 \(n_{123}=4\)，

\[
|A_0|=5.
\tag{2}
\]

字面位置分解为

\[
H_i=A_0\mathbin{\dot\cup}E_i,
\qquad
E_i=\{u_i,v_j,v_k\},
\qquad
\{i,j,k\}=\{1,2,3\}.
\tag{3}
\]

三个 endpoint 都满足

\[
\sigma(H_i)=3a.
\tag{4}
\]

沿 \(m=3\) fringe 等和记

\[
\sigma(v_t)=\sigma(u_t)+\Delta,
\qquad
\delta=\rho(\Delta).
\tag{5}
\]

再用唯一尾的完整实际和

\[
\sigma(U)=3a-4x.
\tag{6}
\]

由
\[
\sigma(E_i)=\sigma(U)+2\Delta
\tag{7}
\]
得到严格实际等式

\[
\boxed{\sigma(A_0)=4x-2\Delta.}
\tag{8}
\]

## 2. 值 \(2\delta\) 的三位置表示

对 \(S\subseteq U\cup V\)、\(1\le|S|\le3\)，沿前稿写
\(S=R(I,J)\)。于是

\[
\rho(\sigma(S))=w(I)+w(J)+|J|\delta.
\tag{9}
\]

在核曲线 \(q_0(\delta)=3\) 上分类

\[
\rho(\sigma(S))=2\delta
\tag{10}
\]

可得：

1. 若 \(|J|=0\)，则需要 \(q_0(w(I))=q_0(2\delta)=12\)，但尾
   子集和的 \(q_0\)-值只有 0 或 1；
2. 若 \(|J|=3\)，由 \(|S|\le3\) 必有 \(I=\varnothing\)，继而
   \(3\delta=2\delta\)，与 \(\delta\ne0\) 矛盾；
3. 若 \(|J|=2\)，唯一解是
   \[
   I=\{i\},\qquad J=[3]\setminus\{i\},
   \tag{11}
   \]
   即三个已知的 \(E_i\)；
4. 若 \(|J|=1\)，除上述解外只在
   \[
   \delta=w_j-w_i,\qquad i\ne j
   \tag{12}
   \]
   出现唯一额外三点集
   \[
   \boxed{
   S_{ij}=(U\setminus\{u_i\})\mathbin{\dot\cup}\{v_j\}.
   }
   \tag{13}
   \]

因此 228 个 generic 曲线点只有三个 \(E_i\) 表示 \(2\delta\)；
六个例外点各自恰多一个 \(S_{ij}\)。注意 (13) 与前稿的

\[
R_{ij}=(U\setminus\{u_j\})\mathbin{\dot\cup}\{v_i\}
\tag{14}
\]

索引相反，二者是不同的字面三点集。

## 3. 共同五核给第二张实际 lift 门

固定例外点 \(\delta=w_j-w_i\)，并沿 \(R_{ij}\) 的 lift 记

\[
\Theta_{ij}
=\sigma(v_i)-\sigma(u_j)
=\theta x+\eta a.
\tag{15}
\]

由 (5) 有

\[
\Theta_{ij}
=\Delta+\sigma(u_i)-\sigma(u_j).
\tag{16}
\]

把与 \(A_0\) 字面不交的三点集 \(S_{ij}\) 加到 (8)。直接计算

\[
\sigma(S_{ij})
=\sigma(U)+2\Delta-\Theta_{ij},
\tag{17}
\]

故八位置块

\[
D=A_0\mathbin{\dot\cup}S_{ij}
\tag{18}
\]

满足

\[
\boxed{
\sigma(D)=3a-\Theta_{ij}
=-\theta x+(3-\eta)a.
}
\tag{19}
\]

这里只先得到 \(\rho(\sigma(D))=0\)；不能把 \(D\) 本身未经轴闭合
就直接送入短谱。

令

\[
d\equiv\theta\pmod p,
\qquad 0\le d\le p-1.
\tag{20}
\]

若 \(d\le p-4=229\)，现有重纤维中可以取 \(d\) 个互异 \(X\)-位置，
使

\[
X_d\mathbin{\dot\cup}D
\tag{21}
\]

在相关轴商中零和，长度为 \(8+d\)，完整和为 \((3-\eta)a\)。

- \(d=0\) 时长度为八，只能是 \(F_3\)，故 \(\eta=0\)；
- \(1\le d\le229\) 时长度为 9 至 237，全部落入已审禁窗；
- \(d=230,231,232\) 时现有 \(X\)-位置不足，本门暂不约束 \(\eta\)。

因此共同五核门的精确允许集为

\[
\boxed{
\mathcal G_A
=\{(0,0)\}
\cup
(\{230,231,232\}\times\mathbb F_{233}),
\qquad
|\mathcal G_A|=700.
}
\tag{22}
\]

## 4. 与 \(U\cup V\) 门的交为空

前稿已经独立审定 \(R_{ij}\) 给出的允许集

\[
\begin{array}{c|c}
\theta&\eta\text{ 的允许值}\\ \hline
4&\{-2\}\\
3,2,1&\{-2,-1\}\\
0&\{-1\}\\
5,6,7&\mathbb F_{233}\\
\text{其余}&\varnothing.
\end{array}
\tag{23}
\]

其大小为 707。现在逐项比较 (22)--(23)：

- \(\theta=0\) 时，(22) 要求 \(\eta=0\)，而 (23) 只允许
  \(\eta=-1\)；
- \(\theta=230,231\) 在 (23) 中分别对应需要七个、六个 \(X\)
  位置的长度十、九禁窗，整列为空；
- \(\theta=232=-1\) 对应五个 \(X\) 位置的长度八 \(F_3\)，但
  字面尾 \(R_{ij}\ne U\)，被唯一正核心 \(F_3\) 块排除。

所以

\[
\boxed{\mathcal G_A\cap\mathcal G_R=\varnothing.}
\tag{24}
\]

六个例外点全部不可能。

## 5. 严格削减与边界

共同 endpoint 五核与 \(U\cup V\) 两张实际 lift 门合并，严格得到

\[
\boxed{
234\longrightarrow228,\qquad
39\ S_3\text{ 轨道}\longrightarrow38.
}
\tag{25}
\]

标出 completion 见证端点后，例外轨道原本分裂成三个 pointed
角色，故

\[
\boxed{117\longrightarrow114.}
\tag{26}
\]

这是对 \(m=3\) 参数轨道的真实删除，但每个 outer row 仍可使用
余下 38 个 generic 轨道；没有因此关闭一条 outer row。

下一步只需在 114 个 pointed generic 候选上加载 cancellation line
的普通表示、至少 460 个逐点 complete 删除、统一 \(q\)-高度和共同
核标签。剩余 180 行和全局 \(A_p\) 仍为 **INCOMPLETE**。
