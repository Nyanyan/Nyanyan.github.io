# Egaroucid 5.5.0 / 5.6.0 Benchmarks

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
<td>0.135</td>
<td>27871488</td>
<td>217746000</td>
</tr>
<tr>
<td>#41</td>
<td>22</td>
<td>h4</td>
<td>0</td>
<td>0.199</td>
<td>28862801</td>
<td>151114141</td>
</tr>
<tr>
<td>#42</td>
<td>22</td>
<td>g2</td>
<td>6</td>
<td>0.213</td>
<td>48660062</td>
<td>237366156</td>
</tr>
<tr>
<td>#43</td>
<td>23</td>
<td>c7</td>
<td>-12</td>
<td>0.776</td>
<td>166809244</td>
<td>216917092</td>
</tr>
<tr>
<td>#44</td>
<td>23</td>
<td>d2</td>
<td>-14</td>
<td>0.323</td>
<td>42549145</td>
<td>134649193</td>
</tr>
<tr>
<td>#45</td>
<td>24</td>
<td>b2</td>
<td>6</td>
<td>3.241</td>
<td>912441891</td>
<td>282840015</td>
</tr>
<tr>
<td>#46</td>
<td>24</td>
<td>b3</td>
<td>-8</td>
<td>1.089</td>
<td>227129647</td>
<td>211677210</td>
</tr>
<tr>
<td>#47</td>
<td>25</td>
<td>g2</td>
<td>4</td>
<td>0.852</td>
<td>151105116</td>
<td>180531799</td>
</tr>
<tr>
<td>#48</td>
<td>25</td>
<td>f6</td>
<td>28</td>
<td>3.025</td>
<td>724631805</td>
<td>240661509</td>
</tr>
<tr>
<td>#49</td>
<td>26</td>
<td>e1</td>
<td>16</td>
<td>4.537</td>
<td>1079040603</td>
<td>239043110</td>
</tr>
<tr>
<td>#50</td>
<td>26</td>
<td>d8</td>
<td>10</td>
<td>13.943</td>
<td>3688114040</td>
<td>264912659</td>
</tr>
<tr>
<td>#51</td>
<td>27</td>
<td>a3</td>
<td>6</td>
<td>14.732</td>
<td>2782257813</td>
<td>189153430</td>
</tr>
<tr>
<td>#52</td>
<td>27</td>
<td>a3</td>
<td>0</td>
<td>3.785</td>
<td>604311247</td>
<td>160635631</td>
</tr>
<tr>
<td>#53</td>
<td>28</td>
<td>d8</td>
<td>-2</td>
<td>69.739</td>
<td>11344109584</td>
<td>163022872</td>
</tr>
<tr>
<td>#54</td>
<td>28</td>
<td>c7</td>
<td>-2</td>
<td>63.972</td>
<td>12621020703</td>
<td>197592458</td>
</tr>
<tr>
<td>#55</td>
<td>29</td>
<td>b7</td>
<td>0</td>
<td>458.573</td>
<td>78910958123</td>
<td>172128553</td>
</tr>
<tr>
<td>#56</td>
<td>29</td>
<td>h5</td>
<td>2</td>
<td>25.576</td>
<td>3533955047</td>
<td>138445312</td>
</tr>
<tr>
<td>#57</td>
<td>30</td>
<td>a6</td>
<td>-10</td>
<td>59.654</td>
<td>9948249883</td>
<td>166956162</td>
</tr>
<tr>
<td>#58</td>
<td>30</td>
<td>g1</td>
<td>4</td>
<td>23.824</td>
<td>3949220953</td>
<td>166066227</td>
</tr>
<tr>
<td>#59</td>
<td>34</td>
<td>g8</td>
<td>64</td>
<td>0.043</td>
<td>7096</td>
<td>645090</td>
</tr>
<tr>
<td>All</td>
<td>-</td>
<td>-</td>
<td>-</td>
<td>748.231</td>
<td>130791306291</td>
<td>174800705</td>
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
<td>148</td>
<td>7</td>
<td>145</td>
<td>0.51</td>
</tr>
<tr>
<td>5</td>
<td>107</td>
<td>8</td>
<td>85</td>
<td>0.56</td>
</tr>
<tr>
<td>15</td>
<td>50</td>
<td>11</td>
<td>39</td>
<td>0.56</td>
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
<td>181</td>
<td>10</td>
<td>109</td>
<td>0.62</td>
</tr>
<tr>
<td>5</td>
<td>114</td>
<td>12</td>
<td>74</td>
<td>0.61</td>
</tr>
<tr>
<td>15</td>
<td>52</td>
<td>9</td>
<td>39</td>
<td>0.57</td>
</tr>
</table>

