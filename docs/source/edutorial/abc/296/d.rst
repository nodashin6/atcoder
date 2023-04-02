:author: nodashin
:date: 2023/04/01

##########
D - M\<=ab
##########

************************************************************
`問題 <https://atcoder.jp/contests/abc296/tasks/abc296_d>`__
************************************************************

.. raw:: html

   <details>
   <summary>問題ページを開きます。</summary>
   <br>
   <iframe src="https://atcoder.jp/contests/abc296/tasks/abc296_d" height="600" width="100%">
   問題リンク
   </iframe>
   <br>
   </details>


****
解説
****

.. role:: blue

:math:`1` 以上 :math:`\left\lceil \sqrt{X} \right\rceil` 以下の :math:`a` について，:math:`M \le a \times b` を満たす最小の :math:`b` を列挙します。

考察@例1
==========

:math:`a \times b` の表を考えます。

.. image:: https://drive.google.com/uc?export=view&id=1-3S9u0L-V1sjEcphoewMsey8-vbSdrPV


全探索したものが左の表です。この表を作成しようとすると :math:`O(N^2)` かかります。

着目したいのは初めて :math:`M` 以上となるマスです。
:math:`a` が定まれば，:math:`M \le a \times b` 以上となる最小の :math:`b` は :math:`O(1)` で求まります [1]_ ので，
:math:`1` 以上 :math:`\left\lceil \sqrt{X} \right\rceil` 以下の :math:`a` について探索すれば，計算量 :math:`O(N)` です。

最後に，整数の積は入れ替えても同じなので :math:`a \le b` の場合のみ数えればよく，計算量 :math:`O(\sqrt{X})` になります。


切り上げや切り捨てで悩んだりするようであれば [2]_ ，すべてのケースで :math:`1` から :math:`10^6 = \sqrt{10^{12}}` 以下の :math:`a` を考えれば問題ありません。

----

**注釈**

.. [1] 二分探索で :math:`O(\text{log} N)` も可。
.. [2] `@kyopro_friendsさんのTweet <https://twitter.com/kyopro_friends/status/1642187173385617408>`__