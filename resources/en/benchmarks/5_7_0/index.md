# Egaroucid 5.7.0 Benchmarks

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
<td>0.187</td>
<td>32617519</td>
<td>174425235</td>
</tr>
<tr>
<td>#41</td>
<td>22</td>
<td>h4</td>
<td>0</td>
<td>0.242</td>
<td>26560625</td>
<td>109754648</td>
</tr>
<tr>
<td>#42</td>
<td>22</td>
<td>g2</td>
<td>6</td>
<td>0.36</td>
<td>51191219</td>
<td>142197830</td>
</tr>
<tr>
<td>#43</td>
<td>23</td>
<td>c7</td>
<td>-12</td>
<td>0.929</td>
<td>168771687</td>
<td>181670276</td>
</tr>
<tr>
<td>#44</td>
<td>23</td>
<td>d2</td>
<td>-14</td>
<td>0.626</td>
<td>43705622</td>
<td>69817287</td>
</tr>
<tr>
<td>#45</td>
<td>24</td>
<td>b2</td>
<td>6</td>
<td>4.256</td>
<td>973544606</td>
<td>228746382</td>
</tr>
<tr>
<td>#46</td>
<td>24</td>
<td>b3</td>
<td>-8</td>
<td>2.315</td>
<td>169047118</td>
<td>73022513</td>
</tr>
<tr>
<td>#47</td>
<td>25</td>
<td>g2</td>
<td>4</td>
<td>0.816</td>
<td>115350803</td>
<td>141361278</td>
</tr>
<tr>
<td>#48</td>
<td>25</td>
<td>f6</td>
<td>28</td>
<td>4.137</td>
<td>822747204</td>
<td>198875321</td>
</tr>
<tr>
<td>#49</td>
<td>26</td>
<td>e1</td>
<td>16</td>
<td>6.387</td>
<td>1021389690</td>
<td>159916970</td>
</tr>
<tr>
<td>#50</td>
<td>26</td>
<td>d8</td>
<td>10</td>
<td>15.945</td>
<td>3470416861</td>
<td>217649223</td>
</tr>
<tr>
<td>#51</td>
<td>27</td>
<td>a3</td>
<td>6</td>
<td>19.308</td>
<td>2093326335</td>
<td>108417564</td>
</tr>
<tr>
<td>#52</td>
<td>27</td>
<td>a3</td>
<td>0</td>
<td>7.95</td>
<td>666596389</td>
<td>83848602</td>
</tr>
<tr>
<td>#53</td>
<td>28</td>
<td>d8</td>
<td>-2</td>
<td>67.989</td>
<td>12227417145</td>
<td>179844050</td>
</tr>
<tr>
<td>#54</td>
<td>28</td>
<td>c7</td>
<td>-2</td>
<td>71.954</td>
<td>13290990536</td>
<td>184715103</td>
</tr>
<tr>
<td>#55</td>
<td>29</td>
<td>b7</td>
<td>0</td>
<td>276.5</td>
<td>41506305139</td>
<td>150113219</td>
</tr>
<tr>
<td>#56</td>
<td>29</td>
<td>h5</td>
<td>2</td>
<td>28.172</td>
<td>3409497345</td>
<td>121024327</td>
</tr>
<tr>
<td>#57</td>
<td>30</td>
<td>a6</td>
<td>-10</td>
<td>88.863</td>
<td>13317806725</td>
<td>149868974</td>
</tr>
<tr>
<td>#58</td>
<td>30</td>
<td>g1</td>
<td>4</td>
<td>31.941</td>
<td>4861384409</td>
<td>152198879</td>
</tr>
<tr>
<td>#59</td>
<td>34</td>
<td>g8</td>
<td>64</td>
<td>1.624</td>
<td>2975</td>
<td>1831</td>
</tr>
<tr>
<td>All</td>
<td>-</td>
<td>-</td>
<td>-</td>
<td>630.501</td>
<td>98268669952</td>
<td>155858072</td>
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
<td>61</td>
<td>2</td>
<td>67</td>
<td>0.48</td>
</tr>
<tr>
<td>5</td>
<td>68</td>
<td>6</td>
<td>56</td>
<td>0.55</td>
</tr>
<tr>
<td>11</td>
<td>69</td>
<td>18</td>
<td>43</td>
<td>0.62</td>
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
<td>76</td>
<td>3</td>
<td>51</td>
<td>0.6</td>
</tr>
<tr>
<td>5</td>
<td>67</td>
<td>11</td>
<td>52</td>
<td>0.56</td>
</tr>
<tr>
<td>11</td>
<td>61</td>
<td>15</td>
<td>54</td>
<td>0.53</td>
</tr>
</table>

