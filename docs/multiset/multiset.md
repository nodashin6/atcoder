# SortedMultiset

[source](../../lib/multiset/multiset.py)


<hr>

## 1. 概要
$\sqrt{N}$ 個のバケットに分割したSortedMultisetです。
bucket indexのイテレーションに $\sqrt[4]{N}$ ごとにスキップ接続を加えたことで，高速化を図っています。

競プロではすでに有名な軽量コードかつ高速な [tatyam](https://twitter.com/tatyam_prime) 氏の [SortedMultiset](https://github.com/tatyam-prime/SortedSet) があり，
安心かつ高速なので，そちらを使用する方が多くの場合で最良の選択肢となります。

### 1-1. スキップ接続
下のブロックにあるSortedMultisetでindex 44の要素にアクセスする際は，  
bucket index 0 からスタートして，bucket_index 8 を探すために8回のイテレーションが必要です。  
しかし，bucket index 0, 3, 6 に対し，スキップ接続を図ることので，bucket_index 0->3->6->7->8の順に移動できます。  
結果として，最大でも $2 \times \sqrt[4]{N}$ 回のイテレーションでbucket_indexを探すことができます。

```
SortedMultiset(
+---[ 0,  1,  2,  3,  4],  # bucket index: 0
|   [ 5,  6,  7,  8,  9],  # bucket index: 1
|   [10, 11, 12, 13, 14],  # bucket index: 2
+---[15, 16, 17, 18, 19],  # bucket index: 3
|   [20, 21, 22, 23, 24],  # bucket index: 4
|   [25, 26, 27, 28, 29],  # bucket index: 5
+---[30, 31, 32, 33, 34],  # bucket index: 6
    [35, 36, 37, 38, 39],  # bucket index: 7
    [40, 41, 42, 43, 44]   # bucket index: 8
)
```

### 1-2. 長所
num_bucket : bucket_size = $\sqrt{N} : \sqrt{N}$ にすることで，  
num_bucket : bucket_size = $\sqrt[3]{N} : \sqrt[3]{N^2}$ の分割では  
遅くなりがちな要素の削除が速くなります。

randomな整数を $N$ 個入れたときの num_bucket と bucket_size
|           $N$|num_bucket|bucket_size|
|:------------:|:--------:|:---------:|
|$1\times 10^3$|         4|      250.0|
|$1\times 10^4$|        32|      321.5|
|$1\times 10^5$|       343|      291.5|
|$2\times 10^5$|       738|      271.0|
|$5\times 10^5$|      1325|      377.4|
|$1\times 10^6$|      1997|      500.8|
|$2\times 10^6$|      1956|     1022.5|
|$5\times 10^6$|      4134|     1209.5|

### 1-3. 短所
長所以外。とくにコードが多い。

<hr>

## 2. 計算量
|関数|計算量|
|:--:|:--:|
|getitem|$O(\sqrt[4]{N})$|
|add|$O(\sqrt{N})$|
|insert|$O(\sqrt{N})$|
|append| $O(1)$|
|appendleft| $O(\sqrt{N})$|
|lower_bound, upper_bound|$O(\sqrt[4]{N} + \log N)$|
|count|$O(\sqrt[4]{N} + \log N)$|
|ge, gt, le, lt|$O(\log N)$|
|pop, popleft|$O(\sqrt{N})$|
|discard|$O(\sqrt{N})$|
|contains|$O(\log N)$|

<hr>

## 3. メソッド
- `add`
- `insert`
- `append`
- `appendleft`
- `lower_bound`
- `upper_bound`
- `count`
- `ge`
- `gt`
- `le`
- `lt`
- `pop`
- `popleft`
- `discard`
- `flatten`


<hr>

## 4. クラスメソッド
- `cls.count_inversion(a=[], count_duplicate=False) -> int`  
転倒数を数えます。BinaryIndexedTree で数えるより遅い気がします。
`count_duplicate=True` では，全く同じ値でも転倒数として扱います。

- `cls.with_bitmask(a=[], base=30) -> SortedMultiset`  
長さ2の配列を要素としてSortedMultisetに入れたいということは非常によくあります。
要素が全てint型で長さが2であれば，bitmaskした`int`型でデータを保持することが可能です。
ユーザーはあたかも内部で配列をそのまま保持しているかのように，要素の追加，削除，検索ができます。

<hr>

## 5. 内部の処理について
### 5-1. バケット分割の仕組み
SortedMultiset内の全要素数 $N$ に関連して，内部に3つの閾値 $M_1, M_2, M_4$ があり，以下の関係性をを満たします。
$$M_1 = \displaystyle \frac{M_2}{2},\space M_2 = \displaystyle \frac{M_4}{2},\space M_2 \sim \sqrt{N}$$
$M_2$ は望ましいバケットサイズであり，その2倍にあたる $M_4$ は大きすぎるバケット，逆に半分の $M_1$ は少ないバケットとなります。
あるバケットに要素を追加した際にそのバケットサイズが $M_4$ を超えたとき，全バケットのサイズが $M_2$ 以下になるように分割します。バケットサイズ $X$ が $M_2$ より大きいバケットは，バケットサイズが $M_1: X-M_1$ に分割されます。この $X-M_1$ がまだ $M_2$ より大きい場合は，さらに $M_1: X-2M_1$ へ分割され，同様にバケットサイズが $M_2$ 以下になるまで分割されます。バケットサイズ $X$ が $M_4$ より大きいバケットは，4つのバケットに分割され， $M_1: M_1: M_1: X-3M_1$ になります。

例) $M_1, M_2, M_4 = 2, 4, 8$ のとき，バケットサイズがそれぞれ(9, 5, 1)である以下のSortedMultisetは，バケットサイズ (2, 2, 2, 3, 2, 3, 1) へと分割されます。
```
# 分割前
SortedMultiset(
    [ 0,  1,  2,  3,  4,  5,  6,  7,  8],
    [ 9, 10, 11, 12, 13],
    [14]
)
# 分割後
SortedMultiset(
    [ 0,  1],
    [ 2,  3],
    [ 4,  5],
    [ 6,  7,  8],
    [ 9, 10],
    [11, 12, 13],
    [14]
)
```


### 5-2. バケットの結合
各バケットから一様に要素を削除していくと，バケット数に比べてバケットサイズが小さいという現象が発生します。バケットの要素がゼロになる度に スキップ接続のためのバケットサイズの計算処理が必要になるため，不用意にバケット数が多くなることは望ましくありません。そのため，一定回数の再構築が行われるとバケットの結合処理が発生します。これは隣接する2つのバケットサイズの和が $M_1$ 未満であるとき，バケットを1つに結合する処理です。

例) $M_1 = 6$ のとき，バケットサイズがそれぞれ(1, 1, 2, 2, 3, 5, ...)である以下のSortedMultisetは，バケットサイズ (4, 5, 5, ...) へ結合されます。
```
# 結合前
SortedMultiset(
    [ 0],
    [ 1],
    [ 2,  3],
    [ 4,  5],
    [ 6,  7,  8],
    [ 9, 10, 11, 12, 13],
    ...
)
# 結合後
SortedMultiset(
    [ 0,  1,  2,  3],
    [ 4,  5,  6,  7,  8],
    [ 9, 10, 11, 12, 13],
    ...
)
```

<hr>

## 6. 処理時間
- 環境: PyPy (7.3.0, on AtCoder)
- テストコード: 下記記載

|functions|$2\times 10^5$|$5\times 10^5$|
|:-------------:|:---------:|:---------:|
|insert         |  0.154 sec|  0.351 sec|
|loc[0]         |  0.006 sec|  0.006 sec|
|loc[i]         |  0.059 sec|  0.109 sec|
|loc[-1]        |  0.048 sec|  0.101 sec|
|lower_bound    |  0.135 sec|  0.322 sec|
|upper_bound    |  0.216 sec|  0.629 sec|
|count          |  0.324 sec|  0.904 sec|
|containts      |  0.149 sec|  0.365 sec|
|gt             |  0.153 sec|  0.384 sec|
|ge             |  0.159 sec|  0.406 sec|
|lt             |  0.164 sec|  0.417 sec|
|le             |  0.175 sec|  0.446 sec|
|dicard         |  0.168 sec|  0.399 sec|
|popleft        |  0.037 sec|  0.082 sec|


```python
import math
import bisect
class SortedMultiset():
    ...


import time
from contextlib import contextmanager
@contextmanager
def timer(s=''):
    t0 = time.time()
    yield
    print(f'{time.time() - t0:.3f} sec    {s}'.rstrip())

import random
random.seed(0)
n = 2*10**5
x = [random.randint(0,10**9) for _ in range(n)]

sm = SortedMultiset()
with timer('insert'):
    for xi in x:
        sm.insert(xi)
with timer('loc[0]'):
    for xi in x:
        sm[0]
with timer('loc[i]'):
    for i in range(n):
        sm[i]
with timer('loc[-1]'):
    for xi in x:
        sm[-1]
with timer('lower_bound'):
    for xi in x:
        sm.lower_bound(xi)
with timer('upper_bound'):
    for xi in x:
        sm.upper_bound(xi)
with timer('count'):
    for xi in x:
        sm.count(xi)
with timer('__containts__'):
    for xi in x:
        xi in sm
with timer('gt'):
    for xi in x:
        sm.gt(xi)
with timer('ge'):
    for xi in x:
        sm.ge(xi)
with timer('lt'):
    for xi in x:
        sm.lt(xi)
with timer('le'):
    for xi in x:
        sm.le(xi)
with timer('dicard'):
    for xi in x:
        sm.discard(xi)
sm = SortedMultiset()
[sm.insert(xi) for xi in x]
with timer('popleft'):
    while sm:
        sm.popleft()
```