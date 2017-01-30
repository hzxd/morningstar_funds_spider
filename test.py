# -*- coding:utf-8 -*-

import parse
import string
from HTMLParser import HTMLParser
import requests
import json
import spider
tr_text = """<tr>
                <th align="left" class="str" scope="row">
                    Donald J. Nesbitt
                    <br />
                    <span>
                            04/01/2005
                        &mdash;
                    </span>
                </th>

                <td align="left">
                	<table>
                		<colgroup>
					        <col width="35%">
					            <col width="65%">
					    </colgroup>
					    <tbody>
	                	<tr>
	                		<td colspan = 2>Mr. Nesbitt joined the firm in early 2002 after spending nearly four years at Qwest Communication’s pension plan in Denver, CO, where he managed $6 billion of equities using quantitative approaches that exploit behavioral anomalies. Prior joining Qwest, Mr. Nesbitt spent nine years at the Illinois Teachers’ Retirement System where, as Chief Investment Officer, he was responsible for the management of $20 billion across various asset classes. Mr. Nesbitt holds a B.S.in economics from Saint Cloud State University, and a M.S. in financial analysis from the University of Wisconsin–Milwaukee.<td>
	                	</tr>

	                	<tr align="left" class="hr">
			                <td colspan="2">
			                </td>
			            </tr>

	                	<tr>
	                		<td><span>Certification</span></td>
	                		<td align="right">CFA</td>
	                	</tr>

	                	<tr align="left" class="hr">
			                <td colspan="2">
			                </td>
			            </tr>

	                	<tr>
	                		<td><span>Education</span></td>
	                		<td
	                			>
	                			<table>
	                				<tr>
	                					<td align="right">M.S. University of Wisconsin, Milwaukee, </td>
	                				</tr>
	                				<tr>
	                					<td align="right">B.S. St. Cloud State University, </td>
	                				</tr>
	                			</table>
	                		</td>
	                	</tr>

	                	<tr align="left" class="hr">
			                <td colspan="2">
			                </td>
			            </tr>

				            <tr onclick="collapse('20407')">
		                		<td><span>Other Assets Managed</span></td>
		                		<td align="left">
		                			<div id="open_20407">
		                				<img width="12" height="12" src="//srt.morningstar.com/oprn/static/common/img/acc_close.gif">
		                			</div>
		                			<div id="close_20407" style="display: none;">
		                				<img width="12" height="12" src="//srt.morningstar.com/oprn/static/common/img/acc_open.gif">
		                			</div>
		                		</td>
		                	</tr>
		                	<tr id="otherAssets_20407" style="display:none">
		                		<td colspan="2">
		                			<div id="managedHistory_20407"></div>
		                		</td>
		                	</tr>
	                	</tbody>
                	</table>

                </td>
            </tr>"""


# print parse.get_manager_name(tr_text)
# print parse.get_manager_time(tr_text)
# print parse.get_manager_abstract(tr_text)
# print parse.get_manager_certification(tr_text)
# print parse.get_manager_education(tr_text)
#
# advisor_jsonp = requests.get('http://financials.morningstar.com/oprn/c-advisorInfo.action?&t=F000002OBU&region=usa&culture=en-US&cur=&callback=jsonp')
# advisor = advisor_jsonp.content[6:-1]
# advisor = json.loads(advisor)['html']
#
# print parse.get_fund_inception(advisor)
# print parse.get_fund_subadvisor(advisor)
# print parse.get_fund_name_of_issuer(advisor)
# print parse.get_fund_advisor(advisor)
m = requests.get('http://financials.morningstar.com/oprn/c-managers.action?&t=F000002OBU&region=usa&culture=en-US&cur=&callback=')

print spider.get_manager_info(m.content)
