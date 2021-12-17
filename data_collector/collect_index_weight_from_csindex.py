import requests
import time
import sys
import threading

sys.path.append("..")
import parsers.disguise as disguise
import data_miner.data_miner_common_target_index_operator as target_index_operator
import log.custom_logger as custom_logger

class CollectIndexWeightFromCSIndex:
    # 从中证官网获取指数成分股及权重信息

    def __init__(self):
        # 当天的日期
        self.today = time.strftime("%Y-%m-%d", time.localtime())


    def download_index_weight_file(self, index_code, index_name, header, proxy):
        # 下载指数成分股及权重文件
        # index_code ： 指数代码，如 399997
        # index_name: 指数名称，如 中证白酒指数
        # header，伪装的UA
        # proxy，伪装的IP
        # 返回：下载文件

        # 地址模板
        interface_address = 'https://csi-web-dev.oss-cn-shanghai-finance-1-pub.aliyuncs.com/static/html/csindex/public/uploads/file/autofile/closeweight/'+index_code+'closeweight.xls'

        '''
        herder = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive"
        }
        r = requests.get(interface_address, headers=herder)
        # open打开excel文件，报存为后缀为xls的文件
        fp = open("../data_collector/index_weight_samples/399997.xls", "wb")
        fp.write(r.content)
        fp.close()
        '''
        # 递归算法，处理异常
        try:
            # 增加连接重试次数,默认10次
            requests.adapters.DEFAULT_RETRIES = 10
            # 关闭多余的连接：requests使用了urllib3库，默认的http connection是keep-alive的，
            # requests设置False关闭
            s = requests.session()
            s.keep_alive = False

            # 忽略警告
            requests.packages.urllib3.disable_warnings()

            # 得到接口返回的信息
            file_data = requests.get(interface_address, headers=header, proxies=proxy, verify=False, stream=False,
                                    timeout=10)
            # open打开excel文件，报存为后缀为xls的文件
            fp = open("../data_collector/index_weight_samples/"+index_code+"_"+index_name+"_"+self.today+".xls", "wb")
            fp.write(file_data.content)
            fp.close()
            # 日志记录
            msg = "从中证指数官网下载" + index_code+ index_name + " 指数的权重文件成功"
            custom_logger.CustomLogger().log_writter(msg, lev='warning')

        # 如果读取超时，重新在执行一遍解析页面
        except requests.exceptions.ReadTimeout:
            # 日志记录
            msg = "从中证指数官网"+interface_address+"下载 " + index_code + index_name + "指数的权重文件失败" + "ReadTimeout。正在重试"
            custom_logger.CustomLogger().log_writter(msg, lev='warning')
            # 返回解析页面得到的股票指标
            return self.download_index_weight_file_from_cs_index(index_code,index_name)

        # 如果连接请求超时，重新在执行一遍解析页面
        except requests.exceptions.ConnectTimeout:
            # 日志记录
            msg = "从中证指数官网"+interface_address+"下载 " + index_code + index_name + "指数的权重文件失败" + "ConnectTimeout。正在重试"
            custom_logger.CustomLogger().log_writter(msg, lev='warning')
            # 返回解析页面得到的股票指标
            return self.download_index_weight_file_from_cs_index(index_code,index_name)

        # 如果请求超时，重新在执行一遍解析页面
        except requests.exceptions.Timeout:
            # 日志记录
            msg = "从中证指数官网"+interface_address+"下载 " + index_code + index_name + "指数的权重文件失败" + "Timeout。正在重试"
            custom_logger.CustomLogger().log_writter(msg, lev='warning')
            # 返回解析页面得到的股票指标
            return self.download_index_weight_file_from_cs_index(index_code,index_name)

        except Exception as e:
            # 日志记录
            msg = msg = "从中证指数官网"+interface_address+"下载 " + index_code + index_name + "指数的权重文件失败 " + str(e)+" 正在重试"
            custom_logger.CustomLogger().log_writter(msg, lev='warning')
            # 返回解析页面得到的股票指标
            return self.download_index_weight_file_from_cs_index(index_code,index_name)



    def download_index_weight_file_from_cs_index(self,index_code, index_name):
        # 从中证官网下载 指数成份股及权重信息的文件
        # index_code: 指数代码，如 399997
        # index_name: 指数名称，如 中证白酒指数
        # 返回： 下载文件

        # 伪装，隐藏UA和IP
        ip_address, ua = disguise.Disguise().get_one_IP_UA()
        header = {"user-agent": ua['ua'], 'Connection': 'close'}
        proxy = {'http': 'http://' + ip_address['ip_address']}

        return self.download_index_weight_file(index_code, index_name, header, proxy)

    def get_cs_index_from_index_target(self):
        # 从标的池中获取中证公司的指数
        # 返回：指数代码及对应的指数名称的字典
        # {'399997': '中证白酒指数', '000932': '中证主要消费', '399965': '中证800地产', '399986': '中证银行指数', '000036': '上证主要消费行业指数'}

        # 存放指数代码及对应的指数名称的字典
        target_cs_index_dict = dict()

        #[{'index_code': '399965', 'index_name': '中证800地产', 'index_code_with_init': 'sz399965',
        # 'index_code_with_market_code': '399965.XSHE'},，，]
        target_cs_index_info_list =  target_index_operator.DataMinerCommonTargetIndexOperator().get_given_index_company_index("中证")
        for info in target_cs_index_info_list:
            target_cs_index_dict[info["index_code"]] = info["index_name"]
        return target_cs_index_dict


    def download_all_target_cs_index_weight_single_thread(self):
        # 单线程下载所有的标的池的中证指数权重文件
        # 返回： 下载文件

        # 从标的池中获取中证公司的指数，指数代码及对应的指数名称的字典
        target_cs_index_dict = self.get_cs_index_from_index_target()
        for index_code in target_cs_index_dict:
            # 下载权重文件
            self.download_index_weight_file_from_cs_index(index_code, target_cs_index_dict[index_code])

    def download_all_target_cs_index_weight_multi_threads(self):
        # 多线程下载所有的标的池的中证指数权重文件
        # 返回： 下载文件

        # 从标的池中获取中证公司的指数，指数代码及对应的指数名称的字典
        target_cs_index_dict = self.get_cs_index_from_index_target()

        # 启用多线程
        running_threads = []
        for index_code in target_cs_index_dict:
            # 启动线程
            running_thread = threading.Thread(target=self.download_index_weight_file_from_cs_index,
                                              kwargs={"index_code": index_code, "index_name": target_cs_index_dict[index_code]})
            running_threads.append(running_thread)

        # 开启新线程
        for mem in running_threads:
            mem.start()

        # 等待所有线程完成
        for mem in running_threads:
            mem.join()


if __name__ == '__main__':
    time_start = time.time()
    go = CollectIndexWeightFromCSIndex()
    go.download_all_target_cs_index_weight_multi_threads()
    time_end = time.time()
    print('Time Cost: ' + str(time_end - time_start))
