:author: nodashin
:date: 2023/04/22

#################
F - Rectangle GCD
#################

************************************************************
`問題 <https://atcoder.jp/contests/abc254/tasks/abc254_f>`__
************************************************************

.. raw:: html

   <details>
   <summary>問題ページを開きます。</summary>
   <br>
   <iframe src="https://atcoder.jp/contests/abc254/tasks/abc254_f" height="600" width="100%">
   問題リンク
   </iframe>
   <br>
   </details>


****
解説
****

:math:`\text{gcd}(a, b) = \text{gcd}(a, a-b)` であることを用います。
数列 :math:`A, B` の隣接項の差をセグ木に乗せて，区間 :math:`text{gcd}` を計算します。


上式についての詳しいことはユークリッド互除法あたりを見ると良い気がします。
..

    **ユークリッド互除法**

    自然数 :math:`a, b` :math:`(a \geq b)` の最小公倍数は，:math:`a` を :math:`b` で割ったあまりを :math:`r` とすると，

    .. math::

        \text{gcd}(a, b) = \text{gcd}(b, r)

..



入力例1をそのまま表にすると下記のようになります。

.. csv-table::
    :header: A\, B, 8, 1, 3
    :width: 60%

    **3**, 11,  4,  6
    **5**, 13,  6,  8
    **2**, 10,  3,  5

隣接項の差を次のように求めて，:math:`\text{gcd}(C_{i}, D{i})` を表にするとこんな感じになります。

- :math:`C_{i} = \text{abs}(A_{i+1} - A{i})`
- :math:`D_{i} = \text{abs}(B_{i+1} - B{i})`

.. csv-table::
    :header: C\, D, 7, 2
    :width: 60%

    **2**, 1, 2
    **3**, 1, 1

こうすると隣接する項間の最大公約数を得ます。

ただしこれは，冒頭で述べてた :math:`\text{gcd}(a, b) = \text{gcd}(a, a-b)` の :math:`a-b` の部分です。
そのため，先頭の項 :math:`a` との最大公約数 :math:`\text{gcd}(a, a-b)` を求めて，初めて答えになります。

最大公約数の計算は交換法則が成り立ちますので，セグ木で管理します。