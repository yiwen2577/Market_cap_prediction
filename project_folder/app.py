from flask import Flask, render_template, request, redirect, url_for
import io
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端
import matplotlib.pyplot as plt
import base64
from functions import *
from openai import OpenAI
import re





app = Flask(__name__)

@app.route('/')
def choose_language():
    return render_template('language_yjl.html')

@app.route('/zh',methods=["POST","GET"]) #简体中文
def zh_index():
# '''
#     client = OpenAI()



#     completion = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             {
#                 "role": "user",
#                 "content": "tell me a joke"
#             }
#         ]
#     )

# '''



    generated_text = "暂停使用gpt"


    return render_template('ch_index.html',text=generated_text)



@app.route('/en',methods=["POST","GET"]) #English
def en_index():
# '''
#     client = OpenAI()



#     completion = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             {
#                 "role": "user",
#                 "content": "tell me a joke"
#             }
#         ]
#     )

# '''
    generated_text = "暂停使用gpt"


    return render_template('en_index.html',text=generated_text)




@app.route('/zh/company', methods=['POST'])
def company():
    try:

        company_name = request.form['company_name']
        function_num = int(request.form['function_num'])
        
        # 根据不同的功能号调用相应函数并返回结果
        if function_num == 1:
            result_data = company_profile(company_name)
            key_mapping = {
                "Short Name": "简称",
                "Long Name": "全称",
                "Country": "国家",
                "Website": "官网",
                "Industry": "行业",
                "Sector": "部门",
                "Business Summary": "业务概要",
                "Full-time Employees": "全职员工",
                "Market Cap": "市值",
                "Volume": "交易量",
                "Previous Close": "前收盘价",
                "Current Price": "当前价格",
                "Open": "开盘价",
                "Day Low": "最低价",
                "Day High": "最高价",
                "Error": "错误信息"
            }         
            result_data = dict(map(lambda item: (key_mapping.get(item[0], item[0]), item[1]), result_data.items()))
            result_type = 'simple'  # 简单字典
            
        elif function_num == 2:
            result_data = get_financial_numbers(company_name)
            # 英文到中文的映射字典
            key_mapping_valuation = {
                "Short Name": "简称",
                "Long Name": "全称",
                "Market Cap": "市值",
                "Enterprise Value": "企业价值",
                "Trailing PE": "市盈率（TTM）",
                "Forward PE": "市盈率（预期）",
                "PEG Ratio": "PEG比率",
                "Price to Sales Trailing 12 Months": "市销率（TTM）",
                "Price to Book": "市净率"
            }

            key_mapping_financial = {
                "Short Name": "简称",
                "Long Name": "全称",
                "Profit Margins": "利润率",
                "Return on Assets": "资产回报率",
                "Return on Equity": "股本回报率",
                "Total Revenue": "总收入",
                "Net Income to Common": "归属于普通股股东的净利润",
                "Trailing EPS": "每股收益（TTM）",
                "Forward EPS": "每股收益（预期）",
                "Total Debt/Equity": "资产负债率",
                "Free Cash Flow": "自由现金流"
            }

            # 使用 map 直接转换键
            result_data = {
                "估值指标": list(map(lambda x: [key_mapping_valuation.get(x[0], x[0]), x[1]], result_data['Valuation Measures'])),
                "财务亮点": list(map(lambda x: [key_mapping_financial.get(x[0], x[0]), x[1]], result_data['Financial Highlights']))
            }           
            result_type = 'nested'  # 嵌套字典
            
        elif function_num == 3:
            statement_choice = int(request.form['statement_choice'])
            result_data = get_financial_statements(company_name, statement_choice)
            if statement_choice == 1:
                result = re.split(r'(<th>)', result_data)
                indices = [index for index, value in enumerate(result) if value == '<th>']
                original = [result[indices[i] + 1].split('</th>')[0] for i in range(len(indices))]
                list = [result[indices[i] + 1].split('</th>')[0] for i in range(6,len(indices))]
                trans_map = {
                                "Treasury Shares Number": "库存股数",
                                "Ordinary Shares Number": "普通股数",
                                "Share Issued": "发行股数",
                                "Net Debt": "净债务",
                                "Total Debt": "总债务",
                                "Tangible Book Value": "有形账面价值",
                                "Invested Capital": "投资资本",
                                "Working Capital": "营运资本",
                                "Net Tangible Assets": "净有形资产",
                                "Capital Lease Obligations": "资本租赁义务",
                                "Common Stock Equity": "普通股权益",
                                "Total Capitalization": "总资本化",
                                "Total Equity Gross Minority Interest": "总权益（含少数股东权益）",
                                "Stockholders Equity": "股东权益",
                                "Gains Losses Not Affecting Retained Earnings": "影响未分配利润的收益损失",
                                "Other Equity Adjustments": "其他权益调整",
                                "Retained Earnings": "留存收益",
                                "Capital Stock": "资本股",
                                "Common Stock": "普通股",
                                "Total Liabilities Net Minority Interest": "总负债（净少数股东权益）",
                                "Total Non Current Liabilities Net Minority Interest": "总非流动负债（净少数股东权益）",
                                "Other Non Current Liabilities": "其他非流动负债",
                                "Tradeand Other Payables Non Current": "应付账款及其他非流动负债",
                                "Long Term Debt And Capital Lease Obligation": "长期债务及资本租赁义务",
                                "Long Term Capital Lease Obligation": "长期资本租赁义务",
                                "Long Term Debt": "长期债务",
                                "Current Liabilities": "流动负债",
                                "Other Current Liabilities": "其他流动负债",
                                "Current Deferred Liabilities": "流动递延负债",
                                "Current Deferred Revenue": "流动递延收入",
                                "Current Debt And Capital Lease Obligation": "流动债务及资本租赁义务",
                                "Current Capital Lease Obligation": "流动资本租赁义务",
                                "Current Debt": "流动债务",
                                "Other Current Borrowings": "其他流动借款",
                                "Commercial Paper": "商业票据",
                                "Payables And Accrued Expenses": "应付账款及应计费用",
                                "Payables": "应付账款",
                                "Total Tax Payable": "应付总税额",
                                "Income Tax Payable": "应付所得税",
                                "Accounts Payable": "应付账款",
                                "Total Assets": "总资产",
                                "Total Non Current Assets": "总非流动资产",
                                "Other Non Current Assets": "其他非流动资产",
                                "Non Current Deferred Assets": "非流动递延资产",
                                "Non Current Deferred Taxes Assets": "非流动递延税资产",
                                "Investments And Advances": "投资及预付款",
                                "Other Investments": "其他投资",
                                "Investmentin Financial Assets": "金融资产投资",
                                "Available For Sale Securities": "可供出售证券",
                                "Net PPE": "净固定资产",
                                "Accumulated Depreciation": "累计折旧",
                                "Gross PPE": "总固定资产",
                                "Leases": "租赁",
                                "Other Properties": "其他物业",
                                "Machinery Furniture Equipment": "机器设备及家具",
                                "Land And Improvements": "土地及改良",
                                "Properties": "物业",
                                "Current Assets": "流动资产",
                                "Other Current Assets": "其他流动资产",
                                "Inventory": "存货",
                                "Receivables": "应收账款",
                                "Other Receivables": "其他应收账款",
                                "Accounts Receivable": "应收账款",
                                "Cash Cash Equivalents And Short Term Investments": "现金、现金等价物及短期投资",
                                "Other Short Term Investments": "其他短期投资",
                                "Cash And Cash Equivalents": "现金及现金等价物",
                                "Cash Equivalents": "现金等价物",
                                "Cash Financial": "现金财务"
                            }
                trans_list = [trans_map.get(i, i) for i in list]
                trans= original[:6]+trans_list
                for i, index in enumerate(indices):
                    result[index + 1] = result[index + 1].replace(original[i], trans[i])
                result_data = "".join(result)
            if statement_choice==2:
                result = re.split(r'(<th>)', result_data)
                indices = [index for index, value in enumerate(result) if value == '<th>']
                original = [result[indices[i] + 1].split('</th>')[0] for i in range(len(indices))]
                list = [result[indices[i] + 1].split('</th>')[0] for i in range(6,len(indices))]
                trans_map = {
                'Tax Effect Of Unusual Items': '异常项目的税务影响',
                'Tax Rate For Calcs': '计算用税率',
                'Normalized EBITDA': '标准化EBITDA',
                'Net Income From Continuing Operation Net Minority Interest': '来自持续经营的净收入（扣除少数股东权益）',
                'Reconciled Depreciation': '调整后的折旧',
                'Reconciled Cost Of Revenue': '调整后的收入成本',
                'EBITDA': 'EBITDA',
                'EBIT': 'EBIT',
                'Net Interest Income': '净利息收入',
                'Interest Expense': '利息支出',
                'Interest Income': '利息收入',
                'Normalized Income': '标准化收入',
                'Net Income From Continuing And Discontinued Operation': '来自持续和终止业务的净收入',
                'Total Expenses': '总支出',
                'Total Operating Income As Reported': '报告的总营业收入',
                'Diluted Average Shares': '稀释后的平均股份数',
                'Basic Average Shares': '基本平均股份数',
                'Diluted EPS': '稀释每股收益（EPS）',
                'Basic EPS': '基本每股收益（EPS）',
                'Diluted NI Availto Com Stockholders': '稀释后的可供普通股东的净收入',
                'Net Income Common Stockholders': '普通股股东的净收入',
                'Net Income': '净收入',
                'Net Income Including Noncontrolling Interests': '包括非控股权益的净收入',
                'Net Income Continuous Operations': '持续经营的净收入',
                'Tax Provision': '税收准备金',
                'Pretax Income': '税前收入',
                'Other Income Expense': '其他收入支出',
                'Other Non Operating Income Expenses': '其他非营业收入支出',
                'Net Non Operating Interest Income Expense': '净非营业利息收入支出',
                'Interest Expense Non Operating': '非营业利息支出',
                'Interest Income Non Operating': '非营业利息收入',
                'Operating Income': '营业收入',
                'Operating Expense': '营业费用',
                'Research And Development': '研究与开发',
                'Selling General And Administration': '销售、一般与行政费用',
                'Gross Profit': '毛利润',
                'Cost Of Revenue': '收入成本',
                'Total Revenue': '总收入',
                'Operating Revenue': '营业收入'
            }
                trans_list = [trans_map.get(i, i) for i in list]
                trans= original[:6]+trans_list
                for i, index in enumerate(indices):
                    result[index + 1] = result[index + 1].replace(original[i], trans[i])
                result_data = "".join(result)
            elif statement_choice==3:
                result = re.split(r'(<th>)', result_data)
                indices = [index for index, value in enumerate(result) if value == '<th>']
                original = [result[indices[i] + 1].split('</th>')[0] for i in range(len(indices))]
                list = [result[indices[i] + 1].split('</th>')[0] for i in range(6,len(indices))]
                trans_map = {
                    'Free Cash Flow': '自由现金流',
                    'Repurchase Of Capital Stock': '资本股票回购',
                    'Repayment Of Debt': '债务偿还',
                    'Issuance Of Debt': '债务发行',
                    'Issuance Of Capital Stock': '资本股票发行',
                    'Capital Expenditure': '资本支出',
                    'Interest Paid Supplemental Data': '支付的利息补充数据',
                    'Income Tax Paid Supplemental Data': '支付的所得税补充数据',
                    'End Cash Position': '期末现金余额',
                    'Beginning Cash Position': '期初现金余额',
                    'Changes In Cash': '现金变动',
                    'Financing Cash Flow': '融资现金流',
                    'Cash Flow From Continuing Financing Activities': '持续融资活动的现金流',
                    'Net Other Financing Charges': '净其他融资费用',
                    'Cash Dividends Paid': '支付的现金股息',
                    'Common Stock Dividend Paid': '支付的普通股股息',
                    'Net Common Stock Issuance': '净普通股发行',
                    'Common Stock Payments': '普通股支付',
                    'Common Stock Issuance': '普通股发行',
                    'Net Issuance Payments Of Debt': '净债务发行支付',
                    'Net Short Term Debt Issuance': '净短期债务发行',
                    'Net Long Term Debt Issuance': '净长期债务发行',
                    'Long Term Debt Payments': '长期债务支付',
                    'Long Term Debt Issuance': '长期债务发行',
                    'Investing Cash Flow': '投资现金流',
                    'Cash Flow From Continuing Investing Activities': '持续投资活动的现金流',
                    'Net Other Investing Changes': '净其他投资变动',
                    'Net Investment Purchase And Sale': '净投资买卖',
                    'Sale Of Investment': '投资出售',
                    'Purchase Of Investment': '投资购买',
                    'Net Business Purchase And Sale': '净企业买卖',
                    'Purchase Of Business': '企业购买',
                    'Net PPE Purchase And Sale': '净固定资产买卖',
                    'Purchase Of PPE': '固定资产购买',
                    'Operating Cash Flow': '经营现金流',
                    'Cash Flow From Continuing Operating Activities': '持续经营活动的现金流',
                    'Change In Working Capital': '营运资金变动',
                    'Change In Other Working Capital': '其他营运资金变动',
                    'Change In Other Current Liabilities': '其他流动负债变动',
                    'Change In Other Current Assets': '其他流动资产变动',
                    'Change In Payables And Accrued Expense': '应付账款及应计费用变动',
                    'Change In Payable': '应付账款变动',
                    'Change In Account Payable': '应付账款变动',
                    'Change In Inventory': '存货变动',
                    'Change In Receivables': '应收账款变动',
                    'Changes In Account Receivables': '应收账款变动',
                    'Other Non Cash Items': '其他非现金项目',
                    'Stock Based Compensation': '基于股票的薪酬',
                    'Deferred Tax': '递延税款',
                    'Deferred Income Tax': '递延所得税',
                    'Depreciation Amortization Depletion': '折旧、摊销、耗竭',
                    'Depreciation And Amortization': '折旧与摊销',
                    'Net Income From Continuing Operations': '来自持续经营的净收入'
                }
                trans_list = [trans_map.get(i, i) for i in list]
                trans= original[:6]+trans_list
                for i, index in enumerate(indices):
                    result[index + 1] = result[index + 1].replace(original[i], trans[i])
                result_data = "".join(result)               
            result_type = 'html_table'  # HTML 表格

        elif function_num == 4:
            buffer = plot_income_data_web(company_name)
            img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

            # Pass the base64 string to the template
            return render_template('plot.html', image_data=img_base64,company_name=company_name)
        
        elif function_num == 6:
            ranking_info = ranking(company_name)
            ranking_info.columns = ["市值","类别","类别排名","行业","行业排名"]
            result_data = ranking_info.to_html(classes="table table-striped", index=True)
            result_type = "ranking"
            

        else:
            return "无效的功能编号"
        
        return render_template('ch_result.html', company=company_name, result_data=result_data, result_type=result_type)

    except Exception as e:
        return render_template('error.html', error_message=str(e))
    

# 英文
@app.route('/en/company', methods=['POST'])
def company_en():
    try:

        company_name = request.form['company_name']
        function_num = int(request.form['function_num'])
        
        # 根据不同的功能号调用相应函数并返回结果
        if function_num == 1:
            result_data = company_profile(company_name)
            result_type = 'simple'  # 简单字典
            
        elif function_num == 2:
            result_data = get_financial_numbers(company_name)
            result_type = 'nested'  # 嵌套字典
            
        elif function_num == 3:
            statement_choice = int(request.form['statement_choice'])
            result_data = get_financial_statements(company_name, statement_choice)
            result_type = 'html_table'  # HTML 表格

        elif function_num == 4:
            buffer = plot_income_data_web(company_name)
            img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

            # Pass the base64 string to the template
            return render_template('plot.html', image_data=img_base64,company_name=company_name)
        
        elif function_num == 6:
            ranking_info = ranking(company_name)
            result_data = ranking_info.to_html(classes="table table-striped", index=True)
            result_type = "ranking" 

        else:
            return "无效的功能编号"
        
        return render_template('en_result.html', company=company_name, result_data=result_data, result_type=result_type)

    except Exception as e:
        return render_template('error.html', error_message=str(e))


# @app.route('/zh/financial_statements', methods=['GET', 'POST'])
# def financial_statements():
#     if request.method == 'POST':
#         company_name = request.form['company_name']
#         choice = int(request.form['statement_choice'])

#         # 调用 get_financial_statements 函数获取相应的财务报表
#         result_data = get_financial_statements(company_name, choice)

#         # 将 HTML 表格数据传递给模板
#         return render_template('result.html', company=company_name, result_data=result_data)

#     return render_template('financial_statements.html')





if __name__ == '__main__':
    app.run(debug=True)
