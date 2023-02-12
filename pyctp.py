from ctypes import *
import struct
import time
import os

#资金账号
class AccountData(object):
	def __init__(self):
		# 投资者帐号
		self.accountID = ""
		# 可用资金
		self.available = 0
		# 期货结算准备金
		self.balance = 0
		# 经纪公司代码
		self.brokerID = ""
		# 资金差额
		self.cashIn = 0
		# 平仓盈亏
		self.closeProfit = 0
		# 手续费
		self.commission = 0
		# 信用额度
		self.credit = 0
		# 币种代码
		self.currencyID = ""
		# 当前保证金总额
		self.currMargin = 0
		# 投资者交割保证金
		self.deliveryMargin = 0
		# 入金金额
		self.deposit = 0
		# 动态权益(新增)
		self.dynamicBalance = 0
		# 交易所交割保证金
		self.exchangeDeliveryMargin = 0
		# 交易所保证金
		self.exchangeMargin = 0
		# 浮动盈亏
		self.floatProfit = 0
		# 冻结的资金
		self.frozenCash = 0
		# 冻结的手续费
		self.frozenCommission = 0
		# 冻结的保证金
		self.frozenMargin = 0
		# 货币质押余额
		self.fundMortgageAvailable = 0
		# 货币质入金额
		self.fundMortgageIn = 0
		# 货币质出金额
		self.fundMortgageOut = 0
		# 利息收入
		self.interest = 0
		# 利息基数
		self.interestBase = 0
		# 质押金额
		self.mortgage = 0
		# 可质押货币金额
		self.mortgageableFund = 0
		# 持仓盈亏
		self.positionProfit = 0
		# 上次结算准备金
		self.preBalance = 0
		# 上次信用额度
		self.preCredit = 0
		# 上次存款额
		self.preDeposit = 0
		# 上次货币质入金额
		self.preFundMortgageIn = 0
		# 上次货币质出金额
		self.preFundMortgageOut = 0
		# 上次占用的保证金
		self.preMargin = 0
		# 上次质押金额
		self.preMortgage = 0
		# 基本准备金
		self.reserve = 0
		# 保底期货结算准备金
		self.reserveBalance = 0
		# 风险度(新增)
		self.risk = 0
		# 结算编号
		self.settlementID = 0
		# 特殊产品平仓盈亏
		self.specProductCloseProfit = 0
		# 特殊产品手续费
		self.specProductCommission = 0
		# 特殊产品交易所保证金
		self.specProductExchangeMargin = 0
		# 特殊产品冻结手续费
		self.specProductFrozenCommission = 0
		# 特殊产品冻结保证金
		self.specProductFrozenMargin = 0
		# 特殊产品占用保证金
		self.specProductMargin = 0
		# 特殊产品持仓盈亏
		self.specProductPositionProfit = 0
		# 根据持仓盈亏算法计算的特殊产品持仓盈亏
		self.specProductPositionProfitByAlg = 0
		# 交易日
		self.tradingDay = ""
		# 出金金额
		self.withdraw = 0
		# 可取资金
		self.withdrawQuota = 0

#码表
class Security(object):
	def __init__(self):
		# 组合类型
		self.combinationType = ""
		# 创建日
		self.createDate = ""
		# 交割月
		self.deliveryMonth = 0
		# 交割年份
		self.deliveryYear = 0
		# 结束交割日
		self.endDelivDate = ""
		# 交易所代码
		self.exchangeID = ""
		# 合约在交易所的代码
		self.exchangeInstID = ""
		# 到期日
		self.expireDate = ""
		# 保留小数位数
		self.digit = 0
		# 合约生命周期状态
		self.instLifePhase = ""
		# 合约代码
		self.instrumentID = ""
		# 合约名称
		self.instrumentName = ""
		# 当前是否交易
		self.isTrading = ""
		# 多头保证金率
		self.longMarginRatio = 0
		# 限价单最大下单量
		self.maxLimitOrderVolume = 0
		# 是否使用大额单边保证金算法
		self.maxMarginSideAlgorithm = ""
		# 市价单最大下单量
		self.maxMarketOrderVolume = 0
		# 限价单最小下单量
		self.minLimitOrderVolume = 0
		# 市价单最小下单量
		self.minMarketOrderVolume = 0
		# 上市日
		self.openDate = ""
		# 期权类型
		self.optionsType = ""
		# 持仓日期类型
		self.positionDateType = ""
		# 持仓类型
		self.positionType = ""
		# 最小变动价位
		self.priceTick = 0
		# 产品类型
		self.productClass = ""
		# 产品代码
		self.productID = ""
		# 空头保证金率
		self.shortMarginRatio = 0
		# 开始交割日
		self.startDelivDate = ""
		# 执行价
		self.strikePrice = 0
		# 基础商品代码
		self.underlyingInstrID = ""
		# 基础商品名称
		self.underlyingInstrName = ""
		# 合约基础商品乘数
		self.underlyingMultiple = 0
		# 合约数量乘数
		self.volumeMultiple = 0

#持仓
class InvestorPosition(object):
	def __init__(self):
		# 放弃执行冻结
		self.abandonFrozen = 0
		# 经纪公司代码
		self.brokerID = ""
		# 资金差额
		self.cashIn = 0
		# 平仓金额
		self.closeAmount = 0
		# 平仓盈亏
		self.closeProfit = 0
		# 逐日盯市平仓盈亏
		self.closeProfitByDate = 0
		# 逐笔对冲平仓盈亏
		self.closeProfitByTrade = 0
		# 平仓量
		self.closeVolume = 0
		# 合约代码
		self.code = ""
		# 组合多头冻结
		self.combLongFrozen = 0
		# 组合成交形成的持仓
		self.combPosition = 0
		# 组合空头冻结
		self.combShortFrozen = 0
		# 手续费
		self.commission = 0
		# 交易所保证金
		self.exchangeMargin = 0
		# 浮动盈亏
		self.floatProfit = 0
		# 冻结的资金
		self.frozenCash = 0
		# 冻结的手续费
		self.frozenCommission = 0
		# 冻结的保证金
		self.frozenMargin = 0
		# 投机套保标志
		self.hedgeFlag = ""
		# 投资者代码
		self.investorID = ""
		# 多头冻结
		self.longFrozen = 0
		# 多头冻结金额
		self.longFrozenAmount = 0
		# 保证金
		self.margin = 0
		# 保证金率
		self.marginRateByMoney = 0
		# 保证金率(按手数)
		self.marginRateByVolume = 0
		# 开仓金额
		self.openAmount = 0
		# 开仓成本
		self.openCost = 0
		# 开仓价格
		self.openPrice = 0
		# 开仓量
		self.openVolume = 0
		# 今日持仓
		self.position = 0
		# 持仓日期
		self.positionDate = ""
		# 持仓多空方向
		self.posiDirection = ""
		# 持仓成本
		self.positionCost = 0
		# 持仓盈亏
		self.positionProfit = 0
		# 上次占用的保证金
		self.preMargin = 0
		# 上次结算价
		self.preSettlementPrice = 0
		# 结算编号
		self.settlementID = 0
		# 本次结算价
		self.settlementPrice = 0
		# 空头冻结
		self.shortFrozen = 0
		# 空头冻结金额
		self.shortFrozenAmount = 0
		# 执行冻结
		self.strikeFrozen = 0
		# 执行冻结金额
		self.strikeFrozenAmount = 0
		# 今日持仓
		self.todayPosition = 0
		# 交易日
		self.tradingDate = ""
		# 占用的保证金
		self.useMargin = 0
		# 上日持仓
		self.ydPosition = 0

#获取组合冻结量
def getFrozenAmount(data):
	posi = 0
	if (data.posiDirection == "多"):
		posi = data.longFrozen
	elif (data.posiDirection == "空"):
		posi = data.shortFrozen
	return posi

#持仓明细
class InvestorPositionDetail(object):
	def __init__(self):
		# 经纪公司代码
		self.brokerID = ""
		# 平仓金额
		self.closeAmount = 0
		# 平仓盈亏
		self.closeProfit = 0
		# 逐日盯市持仓盈亏
		self.closeProfitByDate = 0
		# 逐笔对冲持仓盈亏
		self.closeProfitByTrade = 0
		# 平仓量
		self.closeVolume = 0
		# 合约代码
		self.code = ""
		# 组合合约代码
		self.combInstrumentID = ""
		# 买卖
		self.direction = ""
		# 交易所代码
		self.exchangeID = ""
		# 交易所保证金
		self.exchMargin = 0
		# 浮动盈亏
		self.floatProfit = 0
		# 投机套保标志
		self.hedgeFlag = ""
		# 投资者代码
		self.investorID = ""
		# 昨收盘
		self.lastPrice = 0
		# 昨结算价
		self.lastSettlementPrice = 0
		# 投资者保证金
		self.margin = 0
		# 保证金率
		self.marginRateByMoney = 0
		# 保证金率(按手数)
		self.marginRateByVolume = 0
		# 内部编号
		self.orderRef = ""
		# 开仓日期
		self.openDate = ""
		# 开仓价
		self.openPrice = 0
		# 开仓量
		self.openVolume = 0
		# 本地持仓号，服务器编写
		self.positionNo = ""
		# 持仓盈亏
		self.positionProfit = 0
		# 逐日盯市持仓利润
		self.positionProfitByDate = 0
		# 逐笔对冲持仓利润
		self.positionProfitByTrade = 0
		# 持仓流号
		self.positionStreamId = 0
		# 昨结算价
		self.preSettlementPrice = 0
		# 持仓盈亏基准价
		self.profitBasePrice = 0
		# 结算编号
		self.settlementID = 0
		# 结算价
		self.settlementPrice = 0
		# 成交日期
		self.tradingDay = ""
		# 成交编号
		self.tradeID = ""
		# 成交类型
		self.tradeType = ""
		# 数量
		self.volume = 0

#委托回报
class OrderInfo(object):
	def __init__(self):
		# 激活时间
		self.activeTime = ""
		# 最后修改交易所交易员代码
		self.activeTraderID = ""
		# 操作用户代码
		self.activeUserID = ""
		# 经纪公司代码
		self.brokerID = ""
		# 经纪公司报单编号
		self.brokerOrderSeq = 0
		# 业务单元
		self.businessUnit = ""
		# 撤销时间
		self.cancelTime = ""
		# 结算会员编号
		self.clearingPartID = ""
		# 客户代码
		self.clientID = ""
		# 合约代码
		self.code = ""
		# 组合投机套保标志
		self.combHedgeFlag = ""
		# 组合开平标志
		self.combOffsetFlag = ""
		# 触发条件
		self.contingentCondition = ""
		# 买卖方向
		self.direction = ""
		# 交易所代码
		self.exchangeID = ""
		# 合约在交易所的代码
		self.exchangeInstID = ""
		# 强平原因
		self.forceCloseReason = ""
		# 前置编号
		self.frontID = 0
		# GTD日期
		self.gTDDate = ""
		# 价格
		self.limitPrice = 0
		# 报单日期
		self.insertDate = ""
		# 委托时间
		self.insertTime = ""
		# 安装编号
		self.installID = ""
		# 投资者代码
		self.investorID = ""
		# 自动挂起标志
		self.isAutoSuspend = 0
		# 互换单标志
		self.isSwapOrder = 0
		# 最小成交量
		self.minVolume = 0
		# 报单提示序号
		self.notifySequence = 0
		# 本地报单编号
		self.orderLocalID = ""
		# 报单价格条件
		self.orderPriceType = ""
		# 报单引用
		self.orderRef = ""
		# 报单状态
		self.orderStatus = ""
		# 报单来源
		self.orderSource = ""
		# 报单提交状态
		self.orderSubmitStatus = ""
		# 报单编号
		self.orderSysID = ""
		# 报单类型
		self.orderType = ""
		# 会员代码
		self.participantID = ""
		# 相关报单
		self.relativeOrderSysID = ""
		# 请求编号
		self.requestID = 0
		# 序号
		self.sequenceNo = 0
		# 会话编号
		self.sessionID = 0
		# 结算编号
		self.settlementID = 0
		# 状态信息
		self.statusMsg = ""
		# 止损价
		self.stopPrice = 0
		# 挂起时间
		self.suspendTime = ""
		# 有效期类型
		self.timeCondition = ""
		# 交易所交易员代码
		self.traderID = ""
		# 交易日
		self.tradingDay = ""
		# 最后修改时间
		self.updateTime = ""
		# 用户强评标志
		self.userForceClose = 0
		# 用户代码
		self.userID = ""
		# 用户端产品信息
		self.userProductInfo = ""
		# 成交量类型
		self.volumeCondition = ""
		# 剩余数量
		self.volumeTotal = 0
		# 数量
		self.volumeTotalOriginal = 0
		# 今成交数量
		self.volumeTraded = 0
		# 郑商所成交数量
		self.zCETotalTradedVolume = 0

#最新数据
class SecurityLatestData(object):
	def __init__(self):
		# 触发日
		self.actionDay = ""
		# 卖1价
		self.askPrice1 = 0
		# 卖2价
		self.askPrice2 = 0
		# 卖3价
		self.askPrice3 = 0
		# 卖4价
		self.askPrice4 = 0
		# 卖5价
		self.askPrice5 = 0
		# 卖1量
		self.askVolume1 = 0
		# 卖2量
		self.askVolume2 = 0
		# 卖3量
		self.askVolume3 = 0
		# 卖4量
		self.askVolume4 = 0
		# 卖5量
		self.askVolume5 = 0
		# 平均价格
		self.averagePrice = 0
		# 买1价
		self.bidPrice1 = 0
		# 买2价
		self.bidPrice2 = 0
		# 买3价
		self.bidPrice3 = 0
		# 买4价
		self.bidPrice4 = 0
		# 买5价
		self.bidPrice5 = 0
		# 买1量
		self.bidVolume1 = 0
		# 买2量
		self.bidVolume2 = 0
		# 买3量
		self.bidVolume3 = 0
		# 买4量
		self.bidVolume4 = 0
		# 买5量
		self.bidVolume5 = 0
		# 最新价
		self.close = 0
		# 合约代码
		self.code = ""
		# 今虚实度
		self.currDelta = 0
		# 交易所ID
		self.exchangeID = ""
		# 交易所InstID
		self.exchangeInstID = ""
		# 最高价
		self.high = 0
		# 昨日收盘价
		self.lastClose = 0
		# 最低价
		self.low = 0
		# 跌停价
		self.lowerLimit = 0
		# 开盘价
		self.open = 0
		# 持仓量
		self.openInterest = 0
		# 昨收盘
		self.preClose = 0
		# 昨虚实度
		self.preDelta = 0
		# 昨持仓量
		self.preOpenInterest = 0
		# 上次结算价
		self.preSettlementPrice = 0
		# 本次结算价
		self.settlementPrice = 0
		# 交易日
		self.tradingDay = ""
		# 成交金额
		self.turnover = 0
		# 最后修改毫秒
		self.updateMillisec = 0
		# 最后修改时间
		self.updateTime = ""
		# 涨停价
		self.upperLimit = 0
		# 成交量
		self.volume = 0

#成交回报
class TradeRecord(object):
	def __init__(self):
		# 经纪公司代码
		self.brokerID = ""
		# /经纪公司报单编号
		self.brokerOrderSeq = 0
		# /业务单元
		self.businessUnit = ""
		# /结算会员编号
		self.clearingPartID = ""
		# /客户代码
		self.clientID = ""
		# 合约代码
		self.code = ""
		# 手续费
		self.commission = 0
		# 买卖方向
		self.direction = ""
		# 市场代码
		self.exchangeID = ""
		# 合约在交易所的代码
		self.exchangeInstID = ""
		# 投机套保标志
		self.hedgeFlag = ""
		# 投资者代码
		self.investorID = ""
		# 开平标志
		self.offsetFlag = ""
		# 本地报单编号
		self.orderLocalID = ""
		# 报单引用
		self.orderRef = ""
		# 报单编号
		self.orderSysID = ""
		# 会员代码
		self.participantID = ""
		# 价格
		self.price = 0
		# 成交价来源
		self.priceSource = ""
		# 序号
		self.sequenceNo = 0
		# 结算编号
		self.settlementID = 0
		# 成交编号
		self.tradeID = ""
		# 交易所交易员代码
		self.traderID = ""
		# 成交时期
		self.tradeDate = ""
		# 成交来源
		self.tradeSource = ""
		# 成交时间
		self.tradeTime = ""
		# 交易日
		self.tradingDay = ""
		# 成交类型
		self.tradeType = ""
		# 交易角色
		self.tradingRole = ""
		# 数量
		self.volume = 0
		# 用户代码
		self.userID = ""

#合约手续费率
class CommissionRate(object):
	def __init__(self):
		#经纪公司代码
		self.brokerID = ""
		#收费方式
		self.calculateMode = ""
		#平仓手续费率
		self.closeRatioByMoney = 0
		#平仓手续费
		self.closeRatioByVolume = 0
		#平今手续费率
		self.closeTodayRatioByMoney = 0
		#平今手续费
		self.closeTodayRatioByVolume = 0
		#平今费
		self.closeTodayFee = 0
		#合约代码
		self.code = ""
		#代码
		self.commodityNo = ""
		#类型
		self.commodityType = ""
		#交易所编号
		self.exchangeNo = ""
		#投资者代码
		self.investorID = ""
		#投资者范围
		self.investorRange = ""
		#来源
		self.matchSource = ""
		#开平费
		self.openCloseFee = 0
		#开仓手续费率
		self.openRatioByMoney = 0
		#开仓手续费
		self.openRatioByVolume = 0

#合约保证金率
class MarginRate(object):
	def __init__(self):
		#经纪公司代码
		self.brokerID = ""
		#收费方式
		self.calculateMode = ""
		#看涨看跌标示
		self.callOrPutFlag = ""
		#合约代码
		self.code = ""
		#代码
		self.commodityNo = ""
		#类型
		self.commodityType = ""
		#合约
		self.contractNo = ""
		#投机套保标志
		self.hedgeFlag = ""
		self.initialMargin =0
		#投资者代码
		self.investorID = ""
		#多头保证金率
		self.longMarginRatioByMoney = 0
		#多头保证金费
		self.longMarginRatioByVolume = 0
		#投资者范围
		self.investorRange = ""
		#是否相对交易所收取
		self.isRelativel = 0
		self.lockMargin = 0
		self.maintenanceMargin = 0
		self.sellInitialMargin = 0
		self.sellMaintenanceMargin = 0
		#空头保证金率
		self.shortMarginRatioByMoney = 0
		#空头保证金费
		self.shortMarginRatioByVolume = 0
		#
		self.strikePrice = ""

#转换成CTP手续费率
def convertToCTPCommissionRate(result):
	cTPCommissionRate = CommissionRate()
	results = str.split(',')
	cTPCommissionRate.code = results[0]
	cTPCommissionRate.investorRange = results[1]
	cTPCommissionRate.brokerID = results[2]
	cTPCommissionRate.investorID = results[3]
	cTPCommissionRate.openRatioByMoney = float(results[4])
	cTPCommissionRate.openRatioByVolume = float(results[5])
	cTPCommissionRate.closeRatioByMoney = float(results[6])
	cTPCommissionRate.closeRatioByVolume = float(results[7])
	cTPCommissionRate.closeTodayRatioByMoney = float(results[8])
	cTPCommissionRate.closeTodayRatioByVolume = float(results[9])

#转换CTP保证金率
def convertToCTPMarginRate(result):
	cTPMarginRate = MarginRate()
	results = str.split(',')
	cTPMarginRate.code = results[0]
	cTPMarginRate.brokerID = results[1]
	cTPMarginRate.investorID = results[2]
	cTPMarginRate.hedgeFlag = results[3]
	cTPMarginRate.longMarginRatioByMoney = float(results[4])
	cTPMarginRate.longMarginRatioByVolume = float(results[5])
	cTPMarginRate.shortMarginRatioByMoney = float(results[6])
	cTPMarginRate.shortMarginRatioByVolume = float(results[7])
	cTPMarginRate.isRelativel = int(results[8])

#转换资金账户结构
def convertToCTPAccountData(str):
	cTPTradingAccount = AccountData()
	results = str.split(',')
	alen = len(results)
	if (alen >= 46):
		cTPTradingAccount.brokerID = results[0]
		cTPTradingAccount.accountID = results[1]
		cTPTradingAccount.preMortgage = float(results[2])
		cTPTradingAccount.preCredit = float(results[3])
		cTPTradingAccount.preDeposit = float(results[4])
		cTPTradingAccount.preBalance = float(results[5])
		cTPTradingAccount.preMargin = float(results[6])
		cTPTradingAccount.interestBase = float(results[7])
		cTPTradingAccount.interest = float(results[8])
		cTPTradingAccount.deposit = float(results[9])
		cTPTradingAccount.withdraw = float(results[10])
		cTPTradingAccount.frozenMargin = float(results[11])
		cTPTradingAccount.frozenCash = float(results[12])
		cTPTradingAccount.frozenCommission = float(results[13])
		cTPTradingAccount.currMargin = float(results[14])
		cTPTradingAccount.cashIn = float(results[15])
		cTPTradingAccount.commission = float(results[16])
		cTPTradingAccount.closeProfit = float(results[17])
		cTPTradingAccount.positionProfit = float(results[18])
		cTPTradingAccount.balance = float(results[19])
		cTPTradingAccount.available = float(results[20])
		cTPTradingAccount.withdrawQuota = float(results[21])
		cTPTradingAccount.reserve = float(results[22])
		cTPTradingAccount.tradingDay = results[23]
		cTPTradingAccount.settlementID = float(results[24])
		cTPTradingAccount.credit = float(results[25])
		cTPTradingAccount.mortgage = float(results[26])
		cTPTradingAccount.exchangeMargin = float(results[27])
		cTPTradingAccount.deliveryMargin = float(results[28])
		cTPTradingAccount.exchangeDeliveryMargin = float(results[29])
		cTPTradingAccount.reserveBalance = float(results[30])
		cTPTradingAccount.currencyID = results[31]
		cTPTradingAccount.preFundMortgageIn = float(results[32])
		cTPTradingAccount.preFundMortgageOut = float(results[33])
		cTPTradingAccount.fundMortgageIn = float(results[34])
		cTPTradingAccount.fundMortgageOut = float(results[35])
		cTPTradingAccount.fundMortgageAvailable = float(results[36])
		cTPTradingAccount.mortgageableFund = float(results[37])
		cTPTradingAccount.specProductMargin = float(results[38])
		cTPTradingAccount.specProductFrozenMargin = float(results[39])
		cTPTradingAccount.specProductCommission = float(results[40])
		cTPTradingAccount.specProductFrozenCommission = float(results[41])
		cTPTradingAccount.specProductPositionProfit = float(results[42])
		cTPTradingAccount.specProductCloseProfit = float(results[43])
		cTPTradingAccount.specProductPositionProfitByAlg = float(results[44])
		cTPTradingAccount.specProductExchangeMargin = float(results[45])
		cTPTradingAccount.dynamicBalance = float(results[46])
		cTPTradingAccount.risk = float(results[47])
		cTPTradingAccount.floatProfit = float(results[48])
	return cTPTradingAccount

#转换深度数据结构
def convertToCTPDepthMarketData(str):
	list = []
	strs = str.split(';')
	alen = len(strs)
	for i in range(alen):
		results = strs[i].split(',')
		if (len(results) >= 43):
			cTPDepthMarketData = SecurityLatestData()
			cTPDepthMarketData.tradingDay = results[0]
			cTPDepthMarketData.code = results[1]
			cTPDepthMarketData.exchangeID = results[2]
			cTPDepthMarketData.exchangeInstID = results[3]
			cTPDepthMarketData.close = float(results[4])
			cTPDepthMarketData.preSettlementPrice = float(results[5])
			cTPDepthMarketData.preClose = float(results[6])
			cTPDepthMarketData.preOpenInterest = float(results[7])
			cTPDepthMarketData.open = float(results[8])
			cTPDepthMarketData.high = float(results[9])
			cTPDepthMarketData.low = float(results[10])
			cTPDepthMarketData.volume = float(results[11])
			cTPDepthMarketData.turnover = float(results[12])
			cTPDepthMarketData.openInterest = float(results[13])
			cTPDepthMarketData.lastClose = float(results[14])
			cTPDepthMarketData.settlementPrice = float(results[15])
			cTPDepthMarketData.upperLimit = float(results[16])
			cTPDepthMarketData.lowerLimit = float(results[17])
			cTPDepthMarketData.preDelta = float(results[18])
			cTPDepthMarketData.currDelta = float(results[19])
			cTPDepthMarketData.updateTime = results[20]
			cTPDepthMarketData.updateMillisec = float(results[21])
			cTPDepthMarketData.bidPrice1 = float(results[22])
			cTPDepthMarketData.bidVolume1 = float(results[23])
			cTPDepthMarketData.askPrice1 = float(results[24])
			cTPDepthMarketData.askVolume1 = float(results[25])
			cTPDepthMarketData.bidPrice2 = float(results[26])
			cTPDepthMarketData.bidVolume2 = float(results[27])
			cTPDepthMarketData.askPrice2 = float(results[28])
			cTPDepthMarketData.askVolume2 = float(results[29])
			cTPDepthMarketData.bidPrice3 = float(results[30])
			cTPDepthMarketData.bidVolume3 = float(results[31])
			cTPDepthMarketData.askPrice3 = float(results[32])
			cTPDepthMarketData.askVolume3 = float(results[33])
			cTPDepthMarketData.bidPrice4 = float(results[34])
			cTPDepthMarketData.bidVolume4 = float(results[35])
			cTPDepthMarketData.askPrice4 = float(results[36])
			cTPDepthMarketData.askVolume4 = float(results[37])
			cTPDepthMarketData.bidPrice5 = float(results[38])
			cTPDepthMarketData.bidVolume5 = float(results[39])
			cTPDepthMarketData.askPrice5 = float(results[40])
			cTPDepthMarketData.askVolume5 = float(results[41])
			cTPDepthMarketData.averagePrice = float(results[42])
			cTPDepthMarketData.actionDay = results[43]
			list.append(cTPDepthMarketData)
	return list

#转换期货信息结构
def convertToCTPInstrumentDatas(str):
	cTPInstrumentDatas = []
	strs = str.split(';')
	alen = len(strs)
	for i in range(alen):
		results = strs[i].split(',')
		if (len(results) >= 30):
			cTPInstrumentData = Security()
			cTPInstrumentData.instrumentID = results[0]
			cTPInstrumentData.exchangeID = results[1]
			cTPInstrumentData.instrumentName = results[2]
			cTPInstrumentData.exchangeInstID = results[3]
			cTPInstrumentData.productID = results[4]
			cTPInstrumentData.productClass = results[5]
			cTPInstrumentData.deliveryYear = float(results[6])
			cTPInstrumentData.deliveryMonth = float(results[7])
			cTPInstrumentData.maxMarketOrderVolume = float(results[8])
			cTPInstrumentData.minMarketOrderVolume = float(results[9])
			cTPInstrumentData.maxLimitOrderVolume = float(results[10])
			cTPInstrumentData.minLimitOrderVolume = float(results[11])
			cTPInstrumentData.volumeMultiple = float(results[12])
			cTPInstrumentData.priceTick = float(results[13])
			cTPInstrumentData.createDate = results[14]
			cTPInstrumentData.openDate = results[15]
			cTPInstrumentData.expireDate = results[16]
			cTPInstrumentData.startDelivDate = results[17]
			cTPInstrumentData.endDelivDate = results[18]
			cTPInstrumentData.instLifePhase = results[19]
			cTPInstrumentData.isTrading = results[20]
			cTPInstrumentData.positionType = results[21]
			cTPInstrumentData.positionDateType = results[22]
			cTPInstrumentData.longMarginRatio = float(results[23])
			cTPInstrumentData.shortMarginRatio = float(results[24])
			cTPInstrumentData.maxMarginSideAlgorithm = results[25]
			cTPInstrumentData.underlyingInstrID = results[26]
			cTPInstrumentData.strikePrice = float(results[27])
			cTPInstrumentData.optionsType = results[28]
			cTPInstrumentData.underlyingMultiple = float(results[29])
			cTPInstrumentData.combinationType = results[30]
			cTPInstrumentDatas.append(cTPInstrumentData)
	return cTPInstrumentDatas

#转换持仓结构
def convertToCTPInvestorPosition(str):
	list = []
	strs = str.split(';')
	alen = len(strs)
	for i in range(alen):
		results = strs[i].split(',')
		if (len(results) >= 42):
			cTPInvestorPosition = InvestorPosition()
			cTPInvestorPosition.code = results[0]
			cTPInvestorPosition.brokerID = results[1]
			cTPInvestorPosition.investorID = results[2]
			cTPInvestorPosition.posiDirection = results[3]
			cTPInvestorPosition.hedgeFlag = results[4]
			cTPInvestorPosition.positionDate = results[5]
			cTPInvestorPosition.ydPosition = float(results[6])
			cTPInvestorPosition.position = float(results[7])
			cTPInvestorPosition.longFrozen = float(results[8])
			cTPInvestorPosition.shortFrozen = float(results[9])
			cTPInvestorPosition.longFrozenAmount = float(results[10])
			cTPInvestorPosition.shortFrozenAmount = float(results[11])
			cTPInvestorPosition.openVolume = float(results[12])
			cTPInvestorPosition.closeVolume = float(results[13])
			cTPInvestorPosition.openAmount = float(results[14])
			cTPInvestorPosition.closeAmount = float(results[15])
			cTPInvestorPosition.positionCost = float(results[16])
			cTPInvestorPosition.preMargin = float(results[17])
			cTPInvestorPosition.useMargin = float(results[18])
			cTPInvestorPosition.frozenMargin = float(results[19])
			cTPInvestorPosition.frozenCash = float(results[20])
			cTPInvestorPosition.frozenCommission = float(results[21])
			cTPInvestorPosition.cashIn = float(results[22])
			cTPInvestorPosition.margin = float(results[23])
			cTPInvestorPosition.floatProfit = float(results[24])
			cTPInvestorPosition.positionProfit = float(results[25])
			cTPInvestorPosition.preSettlementPrice = float(results[26])
			cTPInvestorPosition.settlementPrice = float(results[27])
			cTPInvestorPosition.tradingDate = results[28]
			cTPInvestorPosition.settlementID = float(results[29])
			cTPInvestorPosition.openCost = float(results[30])
			cTPInvestorPosition.exchangeMargin = float(results[31])
			cTPInvestorPosition.combPosition = float(results[32])
			cTPInvestorPosition.combLongFrozen = float(results[33])
			cTPInvestorPosition.combShortFrozen = float(results[34])
			cTPInvestorPosition.closeProfitByDate = float(results[35])
			cTPInvestorPosition.closeProfitByTrade = float(results[36])
			cTPInvestorPosition.todayPosition = float(results[37])
			cTPInvestorPosition.marginRateByMoney = float(results[38])
			cTPInvestorPosition.marginRateByVolume = float(results[39])
			cTPInvestorPosition.strikeFrozen = float(results[40])
			cTPInvestorPosition.strikeFrozenAmount = float(results[41])
			cTPInvestorPosition.abandonFrozen = float(results[42])
			cTPInvestorPosition.openPrice = float(results[43])
			list.append(cTPInvestorPosition)
	return list

#转换持仓明细结构
def convertToCTPInvestorPositionDetail(str):
	list = []
	strs = str.split(';')
	alen = len(strs)
	for i in range(alen):
		results = strs[i].split(',')
		if (len(results) >= 25):
			cTPInvestorPositionDetail = InvestorPositionDetail()
			cTPInvestorPositionDetail.code = results[0]
			cTPInvestorPositionDetail.brokerID = results[1]
			cTPInvestorPositionDetail.investorID = results[2]
			cTPInvestorPositionDetail.hedgeFlag = results[3]
			cTPInvestorPositionDetail.direction = results[4]
			cTPInvestorPositionDetail.openDate = results[5]
			cTPInvestorPositionDetail.tradeID = results[6]
			cTPInvestorPositionDetail.volume = float(results[7])
			cTPInvestorPositionDetail.openPrice = float(results[8])
			cTPInvestorPositionDetail.tradingDay = results[9]
			cTPInvestorPositionDetail.settlementID = float(results[10])
			cTPInvestorPositionDetail.tradeType = results[11]
			cTPInvestorPositionDetail.combInstrumentID = results[12]
			cTPInvestorPositionDetail.exchangeID = results[13]
			cTPInvestorPositionDetail.closeProfitByDate = float(results[14])
			cTPInvestorPositionDetail.closeProfitByTrade = float(results[15])
			cTPInvestorPositionDetail.positionProfitByDate = float(results[16])
			cTPInvestorPositionDetail.positionProfitByTrade = float(results[17])
			cTPInvestorPositionDetail.margin = float(results[18])
			cTPInvestorPositionDetail.exchMargin = float(results[19])
			cTPInvestorPositionDetail.marginRateByMoney = float(results[20])
			cTPInvestorPositionDetail.marginRateByVolume = float(results[21])
			cTPInvestorPositionDetail.lastSettlementPrice = float(results[22])
			cTPInvestorPositionDetail.lastSettlementPrice = float(results[23])
			cTPInvestorPositionDetail.settlementPrice = float(results[24])
			cTPInvestorPositionDetail.closeVolume = float(results[25])
			list.append(cTPInvestorPositionDetail)
	return list

#转换成委托回报结构
def convertToCTPOrder(str):
	cTPOrder = OrderInfo()
	results = str.split(',')
	alen = len(results)
	if (len(results) >= 56):
		cTPOrder.brokerID = results[0]
		cTPOrder.investorID = results[1]
		cTPOrder.code = results[2]
		cTPOrder.orderRef = results[3]
		cTPOrder.userID = results[4]
		cTPOrder.orderPriceType = results[5]
		cTPOrder.direction = results[6]
		cTPOrder.combOffsetFlag = results[7]
		cTPOrder.combHedgeFlag = results[8]
		cTPOrder.limitPrice = float(results[9])
		cTPOrder.volumeTotalOriginal = float(results[10])
		cTPOrder.timeCondition = results[11]
		cTPOrder.gTDDate = results[12]
		cTPOrder.volumeCondition = results[13]
		cTPOrder.minVolume = float(results[14])
		cTPOrder.contingentCondition = results[15]
		cTPOrder.stopPrice = float(results[16])
		cTPOrder.forceCloseReason = results[17]
		cTPOrder.isAutoSuspend = results[18]
		cTPOrder.businessUnit = results[19]
		cTPOrder.requestID = float(results[20])
		cTPOrder.orderLocalID = results[21]
		cTPOrder.exchangeID = results[22]
		cTPOrder.participantID = results[23]
		cTPOrder.clientID = results[24]
		cTPOrder.exchangeInstID = results[25]
		cTPOrder.traderID = results[26]
		cTPOrder.installID = results[27]
		cTPOrder.orderSubmitStatus = results[28]
		cTPOrder.notifySequence = float(results[29])
		cTPOrder.tradingDay = results[30]
		cTPOrder.settlementID = float(results[31])
		cTPOrder.orderSysID = results[32]
		cTPOrder.orderSource = results[33]
		cTPOrder.orderStatus = results[34]
		cTPOrder.orderType = results[35]
		cTPOrder.volumeTraded = float(results[36])
		cTPOrder.volumeTotal = float(results[37])
		cTPOrder.insertDate = results[38]
		cTPOrder.insertTime = results[39]
		cTPOrder.activeTime = results[40]
		cTPOrder.suspendTime = results[41]
		cTPOrder.updateTime = results[42]
		cTPOrder.cancelTime = results[43]
		cTPOrder.activeTraderID = results[44]
		cTPOrder.clearingPartID = results[45]
		cTPOrder.sequenceNo = float(results[46])
		cTPOrder.frontID = float(results[47])
		cTPOrder.sessionID = float(results[48])
		cTPOrder.userProductInfo = results[49]
		cTPOrder.statusMsg = results[50]
		cTPOrder.userForceClose = float(results[51])
		cTPOrder.activeUserID = results[52]
		cTPOrder.brokerOrderSeq = float(results[53])
		cTPOrder.relativeOrderSysID = results[54]
		cTPOrder.zCETotalTradedVolume = float(results[55])
		cTPOrder.isSwapOrder = float(results[56])
	return cTPOrder

#转换成委托回报列表
def convertToCTPOrderList(str):
	lst = []
	strs = str.split(';')
	alen = len(strs)
	for i in range(alen):
		lst.append(convertToCTPOrder(strs[i]))
	return lst

#转换成成交回报结构
def convertToCTPTrade(str):
	cTPTrade = TradeRecord()
	results = str.split(',')
	alen = len(results)
	if (len(results) > 30):
		cTPTrade.brokerID = results[0]
		cTPTrade.investorID = results[1]
		cTPTrade.code = results[2]
		cTPTrade.orderRef = results[3]
		cTPTrade.userID = results[4]
		cTPTrade.exchangeID = results[5]
		cTPTrade.tradeID = results[6]
		cTPTrade.direction = results[7]
		cTPTrade.orderSysID = results[8]
		cTPTrade.participantID = results[9]
		cTPTrade.clientID = results[10]
		cTPTrade.tradingRole = results[11]
		cTPTrade.exchangeInstID = results[12]
		cTPTrade.offsetFlag = results[13]
		cTPTrade.hedgeFlag = results[14]
		cTPTrade.price = float(results[15])
		cTPTrade.volume = float(results[16])
		cTPTrade.tradeDate = results[17]
		cTPTrade.tradeTime = results[18]
		cTPTrade.tradeType = results[19]
		cTPTrade.priceSource = results[20]
		cTPTrade.traderID = results[21]
		cTPTrade.orderLocalID = results[22]
		cTPTrade.clearingPartID = results[23]
		cTPTrade.businessUnit = results[24]
		cTPTrade.sequenceNo = float(results[25])
		cTPTrade.tradingDay = results[26]
		cTPTrade.settlementID = float(results[27])
		cTPTrade.brokerOrderSeq = float(results[28])
		cTPTrade.tradeSource = results[29]
		cTPTrade.commission = float(results[30])
	return cTPTrade

#转换成成交回报列表
def convertToCTPTradeRecords(str):
	list = []
	strs = str.split(';')
	alen = len(strs)
	for i in range(alen):
		list.append(convertToCTPTrade(strs[i]))
	return list

#调用CTP的DLL
class CTPDLL(object):
	def __init__(self):
		self.m_ctp = None #CTP对象
		self.m_ctpID = 0 #CTP的编号
	#初始化
	def init(self):
		current_file_path = __file__
		current_file_dir = os.path.dirname(current_file_path)
		self.m_ctp = cdll.LoadLibrary(current_file_dir + r"\\iCTP.dll")
		cdll.argtypes = [c_char_p, c_int, c_double, c_long, c_wchar_p]
	#卖平：多单平仓
	#requestID 请求ID c_int
	#code 代码 c_char_p
	#exchangeID 交易所ID c_char_p
	#price 价格 c_double
	#qty 数量 c_int
	#timeCondition 有效期 c_char(51)
	#orderRef 附加信息 c_char_p
	def askClose(self, requestID, code, exchangeID, price, qty, timeCondition, orderRef):
		return self.m_ctp.askClose(self.m_ctpID, c_int(requestID), c_char_p(code.encode('utf-8')), c_char_p(exchangeID.encode('utf-8')), c_double(price), c_int(qty), c_char(timeCondition), c_char_p(orderRef.encode('utf-8')))
	#卖平今仓：平今天的开仓的空单
	#requestID 请求ID c_int
	#code 代码 c_char_p
	#exchangeID 交易所ID c_char_p
	#price 价格 c_double
	#qty 数量 c_int
	#timeCondition 有效期 c_char(51)
	#orderRef 附加信息 c_char_p
	def askCloseToday(self, requestID, code, exchangeID, price, qty, timeCondition, orderRef):
		return self.m_ctp.askCloseToday(self.m_ctpID, c_int(requestID), c_char_p(code.encode('utf-8')), c_char_p(exchangeID.encode('utf-8')), c_double(price), c_int(qty), c_char(timeCondition), c_char_p(orderRef.encode('utf-8')))
	#卖开：空单开仓
	#requestID 请求ID c_int
	#code 代码 c_char_p
	#exchangeID 交易所ID c_char_p
	#price 价格 c_double
	#qty 数量 c_int
	#timeCondition 有效期 c_char(51)
	#orderRef 附加信息 c_char_p
	def askOpen(self, requestID, code, exchangeID, price, qty, timeCondition, orderRef):
		return self.m_ctp.askOpen(self.m_ctpID, c_int(requestID), c_char_p(code.encode('utf-8')), c_char_p(exchangeID.encode('utf-8')), c_double(price), c_int(qty), c_char(timeCondition), c_char_p(orderRef.encode('utf-8')))
	#买平：空单平仓
	#requestID 请求ID c_int
	#code 代码 c_char_p
	#exchangeID 交易所ID c_char_p
	#price 价格 c_double
	#qty 数量 c_int
	#timeCondition 有效期 c_char(51)
	#orderRef 附加信息 c_char_p
	def bidClose(self, requestID, code, exchangeID, price, qty, timeCondition, orderRef):
		return self.m_ctp.bidClose(self.m_ctpID, c_int(requestID), c_char_p(code.encode('utf-8')), c_char_p(exchangeID.encode('utf-8')), c_double(price), c_int(qty), c_char(timeCondition), c_char_p(orderRef.encode('utf-8')))
	#买平今仓：平今天的开仓的空单
	#requestID 请求ID c_int
	#code 代码 c_char_p
	#exchangeID 交易所ID c_char_p
	#price 价格 c_double
	#qty 数量 c_int
	#timeCondition 有效期 c_char(51)
	#orderRef 附加信息 c_char_p
	def bidCloseToday(self, requestID, code, exchangeID, price, qty, timeCondition, orderRef):
		return self.m_ctp.bidCloseToday(self.m_ctpID, c_int(requestID), c_char_p(code.encode('utf-8')), c_char_p(exchangeID.encode('utf-8')), c_double(price), c_int(qty), c_char(timeCondition), c_char_p(orderRef.encode('utf-8')))
	#买开：多单开仓
	#requestID 请求ID c_int
	#code 代码 c_char_p
	#exchangeID 交易所ID c_char_p
	#price 价格 c_double
	#qty 数量 c_int
	#timeCondition 有效期 c_char(51)
	#orderRef 附加信息 c_char_p
	def bidOpen(self, requestID, code, exchangeID, price, qty, timeCondition, orderRef):
		return self.m_ctp.bidOpen(self.m_ctpID, c_int(requestID), c_char_p(code.encode('utf-8')), c_char_p(exchangeID.encode('utf-8')), c_double(price), c_int(qty), c_char(timeCondition), c_char_p(orderRef.encode('utf-8')))
	#撤单
	#requestID 请求ID c_int
	#exchangeID 交易所ID c_char_p
	#orderSysID 委托编号 c_char_p
	#orderRef 附加信息 c_char_p
	def cancelOrder(self, requestID, exchangeID, orderSysID, orderRef):
		return self.m_ctp.cancelOrder(self.m_ctpID, c_int(requestID), c_char_p(exchangeID.encode('utf-8')), c_char_p(orderSysID.encode('utf-8')), c_char_p(orderRef.encode('utf-8')))
	#创建交易
	def create(self):
		return self.m_ctp.create()
	#生成ctp请求编号
	def generateReqID(self):
		return self.m_ctp.generateReqID(self.m_ctpID)
	#是否有新的数据
	def hasNewDatas(self):
		return self.m_ctp.hasNewDatas(self.m_ctpID)
	#获取资金账户信息
	#data 返回数据 create_string_buffer(1024000)
	def getAccountData(self, data):
		return self.m_ctp.getAccountData(self.m_ctpID, data)
	#获取经纪公司ID
	#data 返回数据 create_string_buffer(1024000)
	def getBrokerID(self, data):
		return self.m_ctp.getBrokerID(self.m_ctpID, data)
	#获取手续费率
	#code 代码 c_char_p
	#data 返回数据 create_string_buffer(1024000)
	def getCommissionRate(self, code, data):
		return self.m_ctp.getCommissionRate(self.m_ctpID, c_char_p(code.encode('utf-8')), data)
	#获取深度市场行情
	#data 返回数据 create_string_buffer(1024000)
	def getDepthMarketData(self, data):
		return self.m_ctp.getDepthMarketData(self.m_ctpID, data)
	#获取合约数据
	#data 返回数据 create_string_buffer(1024000)
	def getInstrumentsData(self, data):
		return self.m_ctp.getInstrumentsData(self.m_ctpID, data)
	#获取投资者ID
	#data 返回数据 create_string_buffer(1024000)
	def getInvestorID(self, data):
		return self.m_ctp.getInvestorID(self.m_ctpID, data)
	#获取保证金率
	#code 代码 c_char_p
	#data 返回数据 create_string_buffer(1024000)
	def getMarginRate(self, code, data):
		return self.m_ctp.getMarginRate(self.m_ctpID,  c_char_p(code.encode('utf-8')), data)
	#获取投资者持仓数据
	#data 返回数据 create_string_buffer(1024000)
	def getPositionData(self, data):
		return self.m_ctp.getPositionData(self.m_ctpID, data)
	#获取投资者持仓明细数据
	#data 返回数据 create_string_buffer(1024000)
	def getPositionDetailData(self, data):
		return self.m_ctp.getPositionDetailData(self.m_ctpID, data)
	#获取最新的委托回报（上一条）
	#data 返回数据 create_string_buffer(1024000)
	def getOrderInfo(self, data):
		return self.m_ctp.getOrderInfo(self.m_ctpID, data)
	#获取所有的最新委托回报（今天的所有委托）
	#data 返回数据 create_string_buffer(1024000)
	def getOrderInfos(self, data):
		return self.m_ctp.getOrderInfos(self.m_ctpID, data)
	#获取所有的最新委托回报（今天的所有委托）
	#data 返回数据 create_string_buffer(1024000)
	def getOrderInfos(self, data):
		return self.m_ctp.getOrderInfos(self.m_ctpID, data)
	#获取sessionID
	def getSessionID(self):
		return self.m_ctp.getSessionID(self.m_ctpID)
	#获取结算单信息
	#data 返回数据 create_string_buffer(1024000)
	def getSettlementInfo(self, data):
		return self.m_ctp.getSettlementInfo(self.m_ctpID, data)
	#获取最新成交记录（上一条） 
	#data 返回数据 create_string_buffer(1024000)
	def getTradeRecord(self, data):
		return self.m_ctp.getTradeRecord(self.m_ctpID, data)
	#获取最新交易记录（今天的所有交易）
	#data 返回数据 create_string_buffer(1024000)
	def getTradeRecords(self, data):
		return self.m_ctp.getTradeRecords(self.m_ctpID, data)
	#获取交易日期
	#data 返回数据 create_string_buffer(1024000)
	def getTradingDate(self, data):
		return self.m_ctp.getTradingDate(self.m_ctpID, data)
	#获取交易时间
	#data 返回数据 create_string_buffer(1024000)
	def getTradingTime(self, data):
		return self.m_ctp.getTradingTime(self.m_ctpID, data)
	#当天是否已经结算
	def isClearanced(self, data):
		return self.m_ctp.isClearanced(self.m_ctpID)
	#是否是结算时间
	def isClearanceTime(self):
		return self.m_ctp.isClearanceTime(self.m_ctpID)
	#数据是否准备好
	def isDataOk(self):
		return self.m_ctp.isDataOk(self.m_ctpID)
	#行情数据服务器是否已经登录
	def isMdLogined(self):
		return self.m_ctp.isMdLogined(self.m_ctpID)
	#交易是否已经登录
	def isTdLogined(self):
		return self.m_ctp.isTdLogined(self.m_ctpID)
	#是否是交易时间
	def isTradingTime(self):
		return self.m_ctp.isTradingTime(self.m_ctpID)
	#是否是精确交易时间(去掉集合竞价时间和休息时间)
	#code 代码 c_char_p
	def isTradingTimeExact(self, code):
		return self.m_ctp.isTradingTimeExact(self.m_ctpID,  c_char_p(code.encode('utf-8')))
	#请求手续费率
	#code 代码 c_char_p
	#requestID 请求ID c_int
	def reqCommissionRate(self, code, requestID):
		return self.m_ctp.reqCommissionRate(self.m_ctpID,  c_char_p(code.encode('utf-8')), c_int(requestID))
	#请求确认结算信息
	#requestID 请求ID c_int
	def reqQrySettlementInfoConfirm(self, requestID):
		return self.m_ctp.reqQrySettlementInfoConfirm(self.m_ctpID, c_int(requestID))
	#请求确认结算信息
	#requestID 请求ID c_int
	#tradingDay 交易日 c_char_p
	def reqQrySettlementInfo(self, requestID, tradingDay):
		return self.m_ctp.reqQrySettlementInfo(self.m_ctpID, c_int(requestID),  c_char_p(tradingDay.encode('utf-8')))
	#请求保证金率
	#code 代码 c_char_p
	#requestID 请求ID c_int
	def reqMarginRate(self, code, requestID):
		return self.m_ctp.reqMarginRate(self.m_ctpID, c_char_p(code.encode('utf-8')), c_int(requestID))
	#启动创建的连接(在create后执行)
	#requestID 请求ID c_int
	#appID APPID c_char_p
	#authCode 用户ID c_char_p
	#mdServer 行情地址 c_char_p
	#tdServer 交易地址 c_char_p
	#brokerID 机构号 c_char_p
	#investorID 投资者账号 c_char_p
	#password 密码 c_char_p
	def start(self, requestID, appID, authCode, mdServer, tdServer, brokerID, investorID, password):
		return self.m_ctp.start(self.m_ctpID, c_int(requestID), c_char_p(appID.encode('utf-8')), c_char_p(authCode.encode('utf-8')), c_char_p(mdServer.encode('utf-8')), c_char_p(tdServer.encode('utf-8')), c_char_p(brokerID.encode('utf-8')), c_char_p(investorID.encode('utf-8')), c_char_p(password.encode('utf-8')))
	#订阅多个合约的行情数据
	#requestID 请求ID c_int
	#code 代码 c_char_p
	def subMarketDatas(self, requestID, code):
		return self.m_ctp.subMarketDatas(self.m_ctpID, int(requestID), c_char_p(code.encode('utf-8')))
	#取消订阅多个合约的行情数据
	#requestID 请求ID c_int
	#code 代码 c_char_p
	def unSubMarketDatas(self, requestID, code):
		return self.m_ctp.unSubMarketDatas(self.m_ctpID, int(requestID), c_char_p(code.encode('utf-8')))
