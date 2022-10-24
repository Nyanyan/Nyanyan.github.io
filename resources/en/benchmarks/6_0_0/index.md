# Egaroucid 6.0.0 Benchmarks

## The FFO endgame test suite

<a href="http://radagast.se/othello/ffotest.html" target="_blank" el=”noopener noreferrer”>The FFO endgame test suite</a> is a common benchmark for endgame searching. Computer completely solves each testcase, and find the best move. This benchmark evaluates the exact time for searching and the speed (NPS: Nodes Per Second).

I used Core i9-11900K for testing.

<table>
<tr>
<td>No.</td>
<td>Depth</td>
<td>Best Move</td>
<td>Score</td>
<td>Time (sec)</td>
<td>Nodes</td>
<td>NPS</td>
</tr>
<tr>
<td>#40</td>
<td>20</td>
<td>a2</td>
<td>38</td>
<td>0.102</td>
<td>27060281</td>
<td>265296872</td>
</tr>
<tr>
<td>#41</td>
<td>22</td>
<td>h4</td>
<td>0</td>
<td>0.152</td>
<td>33056487</td>
<td>217476888</td>
</tr>
<tr>
<td>#42</td>
<td>22</td>
<td>g2</td>
<td>6</td>
<td>0.249</td>
<td>60158183</td>
<td>241599128</td>
</tr>
<tr>
<td>#43</td>
<td>23</td>
<td>c7</td>
<td>-12</td>
<td>0.509</td>
<td>123105384</td>
<td>241857335</td>
</tr>
<tr>
<td>#44</td>
<td>23</td>
<td>d2</td>
<td>-14</td>
<td>0.182</td>
<td>19512855</td>
<td>107213489</td>
</tr>
<tr>
<td>#45</td>
<td>24</td>
<td>b2</td>
<td>6</td>
<td>1.555</td>
<td>483588331</td>
<td>310989280</td>
</tr>
<tr>
<td>#46</td>
<td>24</td>
<td>b3</td>
<td>-8</td>
<td>0.614</td>
<td>148832967</td>
<td>242398969</td>
</tr>
<tr>
<td>#47</td>
<td>25</td>
<td>g2</td>
<td>4</td>
<td>0.234</td>
<td>35991843</td>
<td>153811294</td>
</tr>
<tr>
<td>#48</td>
<td>25</td>
<td>f6</td>
<td>28</td>
<td>0.962</td>
<td>170617090</td>
<td>177356642</td>
</tr>
<tr>
<td>#49</td>
<td>26</td>
<td>e1</td>
<td>16</td>
<td>1.673</td>
<td>365884607</td>
<td>218699705</td>
</tr>
<tr>
<td>#50</td>
<td>26</td>
<td>d8</td>
<td>10</td>
<td>4.738</td>
<td>1147103368</td>
<td>242107084</td>
</tr>
<tr>
<td>#51</td>
<td>27</td>
<td>e2</td>
<td>6</td>
<td>2.682</td>
<td>590452638</td>
<td>220153854</td>
</tr>
<tr>
<td>#52</td>
<td>27</td>
<td>a3</td>
<td>0</td>
<td>2.66</td>
<td>666160199</td>
<td>250436165</td>
</tr>
<tr>
<td>#53</td>
<td>28</td>
<td>d8</td>
<td>-2</td>
<td>17.028</td>
<td>5055604486</td>
<td>296899488</td>
</tr>
<tr>
<td>#54</td>
<td>28</td>
<td>c7</td>
<td>-2</td>
<td>21.663</td>
<td>7053196821</td>
<td>325587260</td>
</tr>
<tr>
<td>#55</td>
<td>29</td>
<td>g6</td>
<td>0</td>
<td>72.651</td>
<td>16591406135</td>
<td>228371338</td>
</tr>
<tr>
<td>#56</td>
<td>29</td>
<td>h5</td>
<td>2</td>
<td>7.423</td>
<td>1418277387</td>
<td>191065254</td>
</tr>
<tr>
<td>#57</td>
<td>30</td>
<td>a6</td>
<td>-10</td>
<td>13.307</td>
<td>2812414286</td>
<td>211348484</td>
</tr>
<tr>
<td>#58</td>
<td>30</td>
<td>g1</td>
<td>4</td>
<td>11.088</td>
<td>2650627564</td>
<td>239053712</td>
</tr>
<tr>
<td>#59</td>
<td>34</td>
<td>g8</td>
<td>64</td>
<td>0.003</td>
<td>7415</td>
<td>2471666</td>
</tr>
<tr>
<td>All</td>
<td>-</td>
<td>-</td>
<td>-</td>
<td>159.475</td>
<td>39453058327</td>
<td>247393374</td>
</tr>
</table>



## Play against Edax4.4

<a href="https://github.com/abulmo/edax-reversi" target="_blank" el=”noopener noreferrer”>Edax 4.4</a> is one of the best Othello AI in the world.

If I set the game from the very beginning, same line appears a lot. To avoid this, I set the game from many different near-draw lines.

No opening books used.

If Egaroucid Win Ratio is over 0.5, then Egaroucid wins more than Edax do.

I used <a href="https://berg.earthlingz.de/xot/index.php" target="_blank" el=”noopener noreferrer”>XOT</a> for its testcases.

### Egaroucid played Black

<table>
<tr>
<td>Level</td>
<td>Egaroucid Win</td>
<td>Draw</td>
<td>Edax Win</td>
<td>Egaroucid Win Ratio</td>
</tr>
<tr>
<td>1</td>
<td>493</td>
<td>18</td>
<td>489</td>
<td>0.5</td>
</tr>
<tr>
<td>5</td>
<td>590</td>
<td>57</td>
<td>353</td>
<td>0.63</td>
</tr>
<tr>
<td>10</td>
<td>598</td>
<td>115</td>
<td>287</td>
<td>0.68</td>
</tr>
<tr>
<td>15</td>
<td>58</td>
<td>12</td>
<td>30</td>
<td>0.66</td>
</tr>
</table>



### Egaroucid played White

<table>
<tr>
<td>Level</td>
<td>Egaroucid Win</td>
<td>Draw</td>
<td>Edax Win</td>
<td>Egaroucid Win Ratio</td>
</tr>
<tr>
<td>1</td>
<td>526</td>
<td>25</td>
<td>449</td>
<td>0.54</td>
</tr>
<tr>
<td>5</td>
<td>539</td>
<td>52</td>
<td>409</td>
<td>0.57</td>
</tr>
<tr>
<td>10</td>
<td>473</td>
<td>115</td>
<td>412</td>
<td>0.53</td>
</tr>
<tr>
<td>15</td>
<td>49</td>
<td>18</td>
<td>33</td>
<td>0.6</td>
</tr>
</table>



