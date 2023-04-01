:author: nodashin
:date: 2023/04/01

#################
C - Gap Existence
#################

************************************************************
`問題 <https://atcoder.jp/contests/abc296/tasks/abc296_c>`__
************************************************************

.. raw:: html

   <details>
   <summary>問題ページを開きます。</summary>
   <br>
   <iframe src="https://atcoder.jp/contests/abc296/tasks/abc296_c" height="600" width="100%">
   問題リンク
   </iframe>
   <br>
   </details>


****
解説
****

.. code-block:: python

    ans = "No"
    for ai in A:
        for aj in A:
            if ai - aj == X:
                ans = "Yes"

のように二重の ``for`` 文では，計算量が :math:`O(N^2)` かかります。
そこで，式変形をして，

.. math::

    A_i - A_j = X \\
    A_i - X = Aj

にすると，:math:`A_i - X` となる :math:`A_j` が数列 :math:`A` に存在するか検索すれば良いことになります。
このとき，数列 :math:`A` が ``list`` や ``tuple`` であれば，
計算量が :math:`O(N^2)` のままなので ``set`` を用います。
``set`` は，1回あたりの判定が :math:`O(1)` なので，:math:`N` 回の判定が
:math:`O(N)` で実行できます。

.. code-block:: python

    N = int(input())
    a_list = list(map(int, input().split()))
    a_set = set(a_list)

    ans = "No"
    for ai in a_set:
        aj = ai - X
        if aj in a_set:
            ans = "Yes"
    print(ans)

   