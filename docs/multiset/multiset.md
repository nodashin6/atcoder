# SortedMultiset

[source](../../lib/multiset/multiset.py)

## 概要
$\sqrt{N}$ 個のバケットに分割したSortedMultisetです。
bucket indexのイテレーションに $\sqrt[4]{N}$ ごとにスキップ接続を加えたことで，高速化を図っています。

競プロではすでに有名な軽量コードかつ高速な[tatyam氏](https://twitter.com/tatyam_prime)の[SortedMultiset](https://github.com/tatyam-prime/SortedSet)があり，
安心かつ高速なので，そちらを使用する方が多くの場合で最良の選択肢となります。

### スキップ接続
下の図でindex 44の要素にアクセスする際は，bucket index 0 からスタートして，bucket_index 8 を探すために  
8回のイテレーションが必要です。  
しかし，bucket index 0, 3, 6 に対し，スキップ接続がされているので，bucket_index 0->3->6->7->8の順に移動できます。  
結果として， $2 \times \sqrt[4]{N}$ 回のイテレーションでbucket_indexを探すことができます。

```
SortedMultiset(
o---[ 0,  1,  2,  3,  4],  # bucket index: 0
|   [ 5,  6,  7,  8,  9],  # bucket index: 1
|   [10, 11, 12, 13, 14],  # bucket index: 2
o---[15, 16, 17, 18, 19],  # bucket index: 3
|   [20, 21, 22, 23, 24],  # bucket index: 4
|   [25, 26, 27, 28, 29],  # bucket index: 5
o---[30, 31, 32, 33, 34],  # bucket index: 6
    [35, 36, 37, 38, 39],  # bucket index: 7
    [40, 41, 42, 43, 44]   # bucket index: 8
)
```

### 長所
num_bucket : bucket_size = $\sqrt{N} : \sqrt{N}$にすることで，  
num_bucket : bucket_size = $\sqrt[3]{N} : \sqrt[3]{N^2}$ の分割では遅くなりがちな要素の削除が
速くなります。

randomな整数を $N$ 個入れたときの num_bucket と bucket_size
|           $N$|num_bucket|bucket_size|
|:------------:|:--------:|:---------:|
|$1\times 10^3$|         4|      250.0|
|$1\times 10^4$|        32|      321.5|
|$1\times 10^5$|       343|      291.5|
|$2\times 10^5$|       738|      271.0|
|$5\times 10^5$|       751|      665.8|
|$1\times 10^6$|      1307|      765.1|


### 短所
長所以外ほぼ全部

