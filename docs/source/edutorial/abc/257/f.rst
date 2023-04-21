:author: nodashin
:date: 2023/04/21

######################
F - Teleporter Setting
######################

************************************************************
`問題 <https://atcoder.jp/contests/abc257/tasks/abc257_f>`__
************************************************************

.. raw:: html

   <details>
   <summary>問題ページを開きます。</summary>
   <br>
   <iframe src="https://atcoder.jp/contests/abc257/tasks/abc257_f" height="600" width="100%">
   問題リンク
   </iframe>
   <br>
   </details>


****
解説
****

始点と終点が固定されている経路問題なので，

- 始点からBFS
- 終点からBFS
  
は想像に難くないと思います。

そのなかで，まだ片方が決定していない町の中で，

- 最も町 :math:`1` に近い町: :math:`p`
- 最も町 :math:`N` に近い町: :math:`q`

をそれぞれも求めておきます。するとこんな図が書けます。

.. mermaid::

    graph LR
        1(("1"))
        i(("i"))
        p(("p"))
        q(("q"))
        N(("N"))

        1 --->|d1i| i
        1 --->|d1p| p
        i --->|diN| N
        p ===> i
        i ===> q
        q --->|dqN| N


町 :math:`1` から町 :math:`N` に到達する組み合わせのうち，距離が最小となるのは，

- 町 :math:`1` --> 町 :math:`i` --> 町 :math:`N`
- 町 :math:`1` --> 町 :math:`i` --> 町 :math:`q` --> 町 :math:`N`
- 町 :math:`1` --> 町 :math:`p` --> 町 :math:`i` --> 町 :math:`N`
- 町 :math:`1` --> 町 :math:`p` --> 町 :math:`i` --> 町 :math:`q` --> 町 :math:`N`

の４つの経路のうちいずれかになります。この４通りを全て計算すればよいです。それぞれ式になおすと，

- :math:`d_{1i} + d_{iN}`
- :math:`d_{1i} + (1 + d_{qN})`
- :math:`(d_{1p} + 1) + d_{iN}`
- :math:`(d_{1p} + 1) + (1 + d_{qN})`

になります。すべての :math:`i` についてこれらの最小値を求ればよいです。