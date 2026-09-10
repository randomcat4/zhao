# 二次量级近原子与四次量级交换网络

STATUS: PROVED_HERE

设 \(Z\) 是长度 \(3p+4\) 的实际零和原子，\(\mathcal F_3\) 是其中
全部 6--8 项、实际和为 \(3a\) 的短块。令

\[
m_3=\left\lceil\frac{p-1}{20}\right\rceil,
\qquad n=3p+4.
\]

逐点真实度下界给 \(D_3(v)\ge m_3\)。对关联对 \((v,A)\) 双计数，

\[
nm_3\le\sum_{v\in Z}D_3(v)
=\sum_{A\in\mathcal F_3}|A|\le8|\mathcal F_3|.
\]

因此

\[
\boxed{
|\mathcal F_3|\ge
M_p:=\left\lceil\frac{(3p+4)m_3}{8}\right\rceil.}
\]

每个 \(A\in\mathcal F_3\) 的商零和补集 \(Z\setminus A\) 都是
\(C_p^3\) 中长度 \(3p-2,3p-3\) 或 \(3p-4\) 的原子。所以任意
\(3p+4\) 原子都同时携带至少 \(M_p=\Omega(p^2)\) 个不同的近
Davenport 补原子，而不只是一个。

现在取不同 \(A,A'\in\mathcal F_3\)，写

\[
I=A\cap A',\qquad J=A\setminus A',\qquad K=A'\setminus A.
\]

同和反链说明 \(J,K\ne\varnothing\)，而商交非零给
\(\bar\sigma(I)\ne0\)。又因两块商和都为零，

\[
\bar\sigma(J)=\bar\sigma(K),
\qquad2\le|J|+|K|\le14.
\]

若 \(J_0\subseteq J,K_0\subseteq K\) 满足
\(\bar\sigma(J_0)=\bar\sigma(K_0)\)，定义

\[
P=I\mathbin{\dot\cup}J_0
\mathbin{\dot\cup}(K\setminus K_0).
\]

则 \(P\) 商和为零、非空，且因 \(Z\setminus(A\cup A')\ne\varnothing\)
而是真子集。还有

\[
|P|\le|A\cup A'|\le15\le2p+2.
\]

由 (SQ)，其实际和直接属于 \(\{a,2a,3a\}\)；原子线正系数长度界
再给出

\[
\boxed{
\sigma(P)=\lambda a,\qquad
\lambda\in\{1,2,3\},\qquad |P|\le5+\lambda.}
\]

若 \(\ell(a)=1\)，还精确有
\(\lambda=3+\ell(J_0)-\ell(K_0)\)。

空交换给回 \(A'\)，全交换给回 \(A\)；任何真子交换都产生第三个
受控短块。等价地，对每一对 \(A,A'\)，二至十四项符号关系

\[
\mathcal R_{A,A'}=J(-K)
\]

要么自身是商群原子，要么它的每个真零和子关系都触发上述交换闭包。
由于 \(|\mathcal F_3|\ge M_p\)，这同时施加在至少
\(\binom{M_p}{2}=\Omega(p^4)\) 个无序块对索引的关系实例上；
这里不主张所得有符号序列彼此不同。

因此单个近 Davenport 原子的局部反模型不再是剩余接口：真正需要
实现的是一个二次量级原子族与四次量级短交换关系网，并同时满足
逐三点带符号设计和统一实际标签高度。
