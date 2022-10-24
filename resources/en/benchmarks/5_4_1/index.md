# Egaroucid 5.4.1 Benchmarks

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
<td>0.329</td>
<td>21899271</td>
<td>71800888</td>
</tr>
<tr>
<td>#41</td>
<td>22</td>
<td>h4</td>
<td>0</td>
<td>0.571</td>
<td>29195205</td>
<td>53373318</td>
</tr>
<tr>
<td>#42</td>
<td>22</td>
<td>g2</td>
<td>6</td>
<td>0.675</td>
<td>38560430</td>
<td>59232611</td>
</tr>
<tr>
<td>#43</td>
<td>23</td>
<td>g3</td>
<td>-12</td>
<td>1.359</td>
<td>103808885</td>
<td>77759464</td>
</tr>
<tr>
<td>#44</td>
<td>23</td>
<td>d2</td>
<td>-14</td>
<td>0.708</td>
<td>29233404</td>
<td>42738894</td>
</tr>
<tr>
<td>#45</td>
<td>24</td>
<td>b2</td>
<td>6</td>
<td>7.027</td>
<td>740350828</td>
<td>105764404</td>
</tr>
<tr>
<td>#46</td>
<td>24</td>
<td>b3</td>
<td>-8</td>
<td>2.009</td>
<td>125044941</td>
<td>63122130</td>
</tr>
<tr>
<td>#47</td>
<td>25</td>
<td>g2</td>
<td>4</td>
<td>0.77</td>
<td>45921608</td>
<td>61722591</td>
</tr>
<tr>
<td>#48</td>
<td>25</td>
<td>f6</td>
<td>28</td>
<td>10.347</td>
<td>1144183176</td>
<td>110902701</td>
</tr>
<tr>
<td>#49</td>
<td>26</td>
<td>e1</td>
<td>16</td>
<td>7.885</td>
<td>887698342</td>
<td>112996224</td>
</tr>
<tr>
<td>#50</td>
<td>26</td>
<td>d8</td>
<td>10</td>
<td>30.077</td>
<td>2678797208</td>
<td>89150599</td>
</tr>
<tr>
<td>#51</td>
<td>27</td>
<td>e2</td>
<td>6</td>
<td>12.585</td>
<td>960039193</td>
<td>76448414</td>
</tr>
<tr>
<td>#52</td>
<td>27</td>
<td>a3</td>
<td>0</td>
<td>13.495</td>
<td>1000193465</td>
<td>74275468</td>
</tr>
<tr>
<td>#53</td>
<td>28</td>
<td>d8</td>
<td>-2</td>
<td>119.188</td>
<td>12209490563</td>
<td>102463855</td>
</tr>
<tr>
<td>#54</td>
<td>28</td>
<td>c7</td>
<td>-2</td>
<td>135.965</td>
<td>13338877012</td>
<td>98123267</td>
</tr>
<tr>
<td>#55</td>
<td>29</td>
<td>g6</td>
<td>0</td>
<td>778.209</td>
<td>76506263895</td>
<td>98314606</td>
</tr>
<tr>
<td>#56</td>
<td>29</td>
<td>h5</td>
<td>2</td>
<td>35.4</td>
<td>2258792760</td>
<td>63858214</td>
</tr>
<tr>
<td>#57</td>
<td>30</td>
<td>a6</td>
<td>-10</td>
<td>142.756</td>
<td>12676954794</td>
<td>88817109</td>
</tr>
<tr>
<td>#58</td>
<td>30</td>
<td>g1</td>
<td>4</td>
<td>50.923</td>
<td>4423383484</td>
<td>86915361</td>
</tr>
<tr>
<td>#59</td>
<td>34</td>
<td>e8</td>
<td>64</td>
<td>1.614</td>
<td>94965014</td>
<td>59990533</td>
</tr>
<tr>
<td>All</td>
<td>-</td>
<td>-</td>
<td>-</td>
<td>1351.892</td>
<td>129313653478</td>
<td>95653834</td>
</tr>
</table>





## Play against Edax4.4

<a href="https://github.com/abulmo/edax-reversi" target="_blank" el=”noopener noreferrer”>Edax 4.4</a> is one of the best Othello AI in the world.

If I set the game from the very beginning, same line appears a lot. To avoid this, I set the game from many different near-draw lines.

No opening books used.

If Egaroucid Win Ratio is over 0.5, then Egaroucid wins more than Edax do.

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
<td>190</td>
<td>8</td>
<td>202</td>
<td>0.48</td>
</tr>
<tr>
<td>5</td>
<td>179</td>
<td>14</td>
<td>107</td>
<td>0.63</td>
</tr>
<tr>
<td>15</td>
<td>63</td>
<td>11</td>
<td>26</td>
<td>0.71</td>
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
<td>209</td>
<td>13</td>
<td>178</td>
<td>0.54</td>
</tr>
<tr>
<td>5</td>
<td>161</td>
<td>17</td>
<td>122</td>
<td>0.57</td>
</tr>
<tr>
<td>15</td>
<td>52</td>
<td>11</td>
<td>37</td>
<td>0.58</td>
</tr>
</table>
