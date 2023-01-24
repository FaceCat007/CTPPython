# -*- coding:utf-8 -*-
#! python3

# FaceCat-Python-Wasm(OpenSource)
#Shanghai JuanJuanMao Information Technology Co., Ltd 

import win32gui
import win32api
from win32con import *
from xml.etree import ElementTree as ET
import math
import requests
import time
from requests.adapters import HTTPAdapter
from facecat import *
import facecat
import pyctp
from ctypes import *
import struct
import os
import timer

#更新悬浮状态
#views:视图集合
def updateView(views):
	for i in range(0,len(views)):
		view = views[i]
		if(view.m_dock == "fill"):
			if(view.m_parent != None and view.m_parent.m_type != "split"):
				view.m_location = FCPoint(0, 0)
				view.m_size = FCSize(view.m_parent.m_size.cx, view.m_parent.m_size.cy)
		if(view.m_type == "split"):
			resetSplitLayoutDiv(view)
		elif(view.m_type == "tabview"):
			updateTabLayout(view)
		elif(view.m_type == "layout"):
			resetLayoutDiv(view)
		subViews = view.m_views
		if(len(subViews) > 0):
			updateView(subViews)

#设置属性
#view:视图
#node:xml节点
def setAttribute(view, child):
	if(view.m_paint != None):
		if(view.m_paint.m_defaultUIStyle == "dark"):
			view.m_backColor = "rgb(0,0,0)"
			view.m_borderColor = "rgb(100,100,100)"
			view.m_textColor = "rgb(255,255,255)"
		elif(view.m_paint.m_defaultUIStyle == "light"):
			view.m_backColor = "rgb(255,255,255)"
			view.m_borderColor = "rgb(150,150,150)"
			view.m_textColor = "rgb(0,0,0)"
		for key in child.attrib:
			name = key.lower()
			value = child.attrib[key]
			if(name == "location"):
				view.m_location = FCPoint(int(value.split(',')[0]), int(value.split(',')[1]))
			elif(name == "size"):
				view.m_size = FCSize(int(value.split(',')[0]), int(value.split(',')[1]))
			elif(name == "text"):
				view.m_text = value
			elif(name == "backcolor"):
				lowerStr = value.lower()
				if(lowerStr.find("rgb") == 0):
					view.m_backColor = value
				else:
					view.m_backColor = "none"
			elif(name == "bordercolor"):
				lowerStr = value.lower()
				if(lowerStr.find("rgb") == 0):
					view.m_borderColor = value
				else:
					view.m_borderColor = "none"
			elif(name == "textcolor"):
				lowerStr = value.lower()
				if(lowerStr.find("rgb") == 0):
					view.m_textColor = value
				else:
					view.m_textColor = "none"
			elif(name == "layoutstyle"):
				view.m_layoutStyle = value.lower()
			elif(name == "dock"):
				view.m_dock = value;
			elif(name == "font"):
				family = value.split(',')[0]
				if(family == "Default"):
					family = "Arial"
				view.m_font = value.split(',')[1] + "px " + family
			elif(name == "headerheight"):
				view.m_headerHeight = float(value)
			elif(name == "splitmode"):
				view.m_splitMode = value.lower()
			elif(name == "autowrap"):
				view.m_autoWrap = (value.lower() == "true")
			elif(name == "name"):
				view.m_name = value;
			elif(name == "showvscrollbar"):
				view.m_showVScrollBar = (value.lower() == "true")
			elif(name == "showhscrollbar"):
				view.m_showHScrollBar = (value.lower() == "true")
			elif(name == "visible"):
				view.m_visible =  (value.lower() == "true")
			elif(name == "displayoffset"):
				view.m_visible =  (value.lower() == "true")
			elif(name == "checked"):
				view.m_checked =  (value.lower() == "true")
			elif(name == "buttonsize"):
				view.m_buttonSize = FCSize(int(value.split(',')[0]), int(value.split(',')[1]))
			elif(name == "topmost"):
				view.m_topMost =  (value.lower() == "true")
			elif(name == "selectedindex"):
				view.m_selectedIndex = int(value)
			elif(name == "src"):
				view.m_src = value
			elif(name == "backimage"):
				view.m_backImage = value
			elif(name == "allowdrag"):
				view.m_allowDrag = (value.lower() == "true")
			elif(name == "groupname"):
				view.m_groupName = value
    
#读取Xml
#paint 绘图对象
#node节点
#parent 父视图
def readXmlNode(paint, node, parent):
	for child in node:
		view = None
		typeStr = ""
		nodeName = child.tag.replace("{facecat}", "").lower()
		if(nodeName == "div" or nodeName == "view"):
			if "type" in child.attrib:
				typeStr = child.attrib["type"]
			if(typeStr == "splitlayout"):
				view = FCSplitLayoutDiv()
			elif(typeStr == "layout"):
				view = FCLayoutDiv()
			elif(typeStr == "tab"):
				view = FCTabView()
			elif(typeStr == "tabpage"):
				view = FCTabPage()
			elif(typeStr == "radio"):
				view = FCRadioButton()
				view.m_backColor = "none"
			elif(typeStr == "checkbox"):
				view = FCCheckBox()
				view.m_backColor = "none"
			elif(typeStr == "button"):
				view = FCView()
				view.m_type = "button"
			elif(typeStr == "text" or typeStr == "range" or typeStr == "datetime"):
				view = FCView()
				view.m_type = "textbox"
			else:
				view = FCView()
				view.m_type = "div"
		elif(nodeName == "table"):
			view = FCGrid()
		elif(nodeName == "chart"):
			view = FCChart()
		elif(nodeName == "tree"):
			view = FCTree()
		elif(nodeName == "select"):
			view = FCView()
			view.m_type = "textbox"
		elif(nodeName == "input"):
			if "type" in child.attrib:
				typeStr = child.attrib["type"]
			if(typeStr == "radio"):
				view = FCRadioButton()
				view.m_backColor = "none"
			elif(typeStr == "checkbox"):
				view = FCCheckBox()
				view.m_backColor = "none"
			elif(typeStr == "button"):
				view = FCView()
				view.m_type = "button"
			elif(typeStr == "text" or typeStr == "range" or typeStr == "datetime"):
				view = FCView()
				view.m_type = "textbox"
			else:
				view = FCView()
				view.m_type = "button"
		else:
			view = FCView()
		view.m_paint = paint
		view.m_parent = parent
		setAttribute(view, child)
		if(nodeName == "label"):
			view.m_type = "label"
			view.m_borderColor = "none"
		if(view != None):
			if(typeStr == "tabpage"):
				tabButton = FCView()
				tabButton.m_type = "tabbutton"
				if "headersize" in child.attrib:
					atrHeaderSize = child.attrib["headersize"]
					tabButton.m_size = FCSize(int(atrHeaderSize.split(',')[0]), int(atrHeaderSize.split(',')[1]))
				else:
					tabButton.m_size = FCSize(100, 20)
				if(view.m_paint.m_defaultUIStyle == "dark"):
					tabButton.m_backColor = "rgb(0,0,0)"
					tabButton.m_borderColor = "rgb(100,100,100)"
					tabButton.m_textColor = "rgb(255,255,255)"
				elif(view.m_paint.m_defaultUIStyle == "light"):
					tabButton.m_backColor = "rgb(255,255,255)"
					tabButton.m_borderColor = "rgb(150,150,150)"
					tabButton.m_textColor = "rgb(0,0,0)"
				tabButton.m_text = view.m_text
				tabButton.m_paint = paint
				addTabPage(view.m_parent, view, tabButton)
			else:
				if(parent != None):
					parent.m_views.append(view)
				else:
					paint.m_views.append(view)
			if(typeStr == "splitlayout"):
				if "datumsize" in child.attrib:
					atrDatum = child.attrib["datumsize"]
					view.m_size = FCSize(int(atrDatum.split(',')[0]), int(atrDatum.split(',')[1]))
				splitter = FCView()
				splitter.m_paint = paint
				splitter.m_parent = view
				if(view.m_paint.m_defaultUIStyle == "dark"):
					splitter.m_backColor = "rgb(100,100,100)"
				elif(view.m_paint.m_defaultUIStyle == "light"):
					splitter.m_backColor = "rgb(150,150,150)"
				if "candragsplitter" in child.attrib:
					if(child.attrib["candragsplitter"] == "true"):
						splitter.m_allowDrag = TRUE
				view.m_splitter = splitter
				splitterposition = child.attrib["splitterposition"]
				splitStr = splitterposition.split(',')
				if(len(splitStr) >= 4):
					splitRect = FCRect(float(splitStr[0]), float(splitStr[1]), float(splitStr[2]), float(splitStr[3]))
					splitter.m_location = FCPoint(splitRect.left, splitRect.top)
					splitter.m_size = FCSize(splitRect.right - splitRect.left, splitRect.bottom - splitRect.top)
				else:
					sSize = float(splitStr[1])
					sPosition = float(splitStr[0])
					if(view.m_layoutStyle == "lefttoright" or view.m_layoutStyle == "righttoleft"):
						splitter.m_location = FCPoint(sPosition, 0)
						splitter.m_size = FCSize(sSize, view.m_size.cy)
					else:
						splitter.m_location = FCPoint(0, sPosition)
						splitter.m_size = FCSize(view.m_size.cx, sSize)
				readXmlNode(paint, child, view)
				subViews = view.m_views
				view.m_firstView = subViews[0];
				view.m_secondView = subViews[1];
				view.m_views.append(splitter)
				view.m_oldSize = FCSize(view.m_size.cx, view.m_size.cy)
				resetSplitLayoutDiv(view)
			elif(typeStr == "tab"):
				readXmlNode(paint, child, view)
				tabPages = view.m_tabPages
				if(len(tabPages) > 0):
					tabPages[0].m_visible = TRUE
			elif(nodeName == "table"):
				for tChild in child:
					if(tChild.tag.replace("{facecat}", "") == "tr"):
						for sunNode in tChild:
							sunNodeName = sunNode.tag.lower().replace("{facecat}", "")
							if(sunNodeName == "th"):
								gridColumn = FCGridColumn()
								gridColumn.m_width = 100
								if "text" in  sunNode.attrib:
									gridColumn.m_text = sunNode.attrib["text"]
								view.m_columns.append(gridColumn)
								if(view.m_paint.m_defaultUIStyle == "light"):
									gridColumn.m_backColor = "rgb(230,230,230)"
									gridColumn.m_borderColor = "rgb(150,150,150)"
									gridColumn.m_textColor = "rgb(0,0,0)"
			elif(view.m_type == "textbox"):
				if(paint.m_useGdiPlus and len(view.m_name) > 0):
					view.m_exView = TRUE
					paint.init()
					paint.m_gdiPlusPaint.createView(view.m_type, view.m_name)
					if(view.m_paint.m_defaultUIStyle == "dark"):
						paint.m_gdiPlusPaint.setAttribute(view.m_name, "backcolor", "rgb(0,0,0)")
						paint.m_gdiPlusPaint.setAttribute(view.m_name, "bordercolor", "rgb(100,100,100)")
						paint.m_gdiPlusPaint.setAttribute(view.m_name, "textcolor", "rgb(255,255,255)")
					elif(view.m_paint.m_defaultUIStyle == "light"):
						paint.m_gdiPlusPaint.setAttribute(view.m_name, "backcolor", "rgb(255,255,255)")
						paint.m_gdiPlusPaint.setAttribute(view.m_name, "bordercolor", "rgb(150,150,150)")
						paint.m_gdiPlusPaint.setAttribute(view.m_name, "textcolor", "rgb(0,0,0)")
					for key in child.attrib:
						name = key.lower()
						value = child.attrib[key]
						paint.m_gdiPlusPaint.setAttribute(view.m_name, name, value)
				else:
					view.m_hWnd = win32gui.CreateWindowEx(0, "Edit", view.m_name, WS_VISIBLE|WS_CHILD|SS_CENTERIMAGE, 0, 0, 100, 30, paint.m_hWnd, 0, 0, None)
					win32gui.ShowWindow(view.m_hWnd, SW_HIDE)
					s = win32gui.GetWindowLong(view.m_hWnd, GWL_EXSTYLE)
					win32gui.SetWindowLong(view.m_hWnd, GWL_EXSTYLE, s|ES_CENTER)
					setViewAttribute(view, "text", view.m_text)
			elif(view.m_type == "combobox"):
				#https://blog.csdn.net/qq_31178679/article/details/125883494
				view.m_hWnd = win32gui.CreateWindowEx(0, "ComboBox", view.m_name, WS_VISIBLE | WS_CHILD | WS_BORDER | CBS_HASSTRINGS | CBS_DROPDOWNLIST, 0, 0, 100, 30, paint.m_hWnd, 0, 0, None)
				win32gui.ShowWindow(view.m_hWnd, SW_HIDE)
				cIndex = 0
				for tChild in child:
					if(tChild.tag.replace("{facecat}", "") == "option"):
						if "text" in tChild.attrib:
							win32gui.SendMessage(view.m_hWnd, CB_ADDSTRING, cIndex, tChild.attrib["text"])
							cIndex = cIndex + 1
				if "selectedindex" in child.attrib:
					win32gui.SendMessage(view.m_hWnd, CB_SETCURSEL, int(child.attrib["selectedindex"]), 0)
			else:
				readXmlNode(paint, child, view)

#绘制视图
#view:视图
#paint:绘图对象
#drawRect:区域
def onViewPaint(view, paint, drawRect):
	if(view.m_type == "radiobutton"):
		drawRadioButton(view, paint, drawRect)
	elif(view.m_type == "checkbox"):
		drawCheckBox(view, paint, drawRect)
	elif(view.m_type == "chart"):
		resetChartVisibleRecord(view)
		checkChartLastVisibleIndex(view)
		calculateChartMaxMin(view)
		drawChart(view, paint, drawRect)
	elif(view.m_type == "grid"):
		drawDiv(view, paint, drawRect)
		drawGrid(view, paint, drawRect)
	elif(view.m_type == "tree"):
		drawDiv(view, paint, drawRect)
		drawTree(view, paint, drawRect)
	elif(view.m_type == "label"):
		if(view.m_textColor != "none"):
			tSize = paint.textSize(view.m_text, view.m_font)
			paint.drawText(view.m_text, view.m_textColor, view.m_font, 0, (view.m_size.cy - tSize.cy) / 2)
	elif(view.m_type == "div" or view.m_type =="tabpage" or view.m_type =="tabview" or view.m_type =="layout"):
		drawDiv(view, paint, drawRect)
	elif(view.m_exView):
		if(paint.m_useGdiPlus):
			paint.m_gdiPlusPaint.paintView(view.m_name, 0, 0, view.m_size.cx, view.m_size.cy)
	else:
		drawButton(view, paint, drawRect)

#绘制视图边线
#view:视图
#paint:绘图对象
#drawRect:区域
def onViewPaintBorder(view, paint, drawRect):
	if(view.m_type == "grid"):
		drawGridScrollBar(view, paint, drawRect)
	elif(view.m_type == "tree"):
		drawTreeScrollBar(view, paint, drawRect)
	elif(view.m_type == "div" or view.m_type =="tabpage" or view.m_type =="tabview" or view.m_type =="layout"):
		drawDivScrollBar(view, paint, drawRect)
		drawDivBorder(view, paint, drawRect)

#视图的鼠标移动方法
#view 视图
#mp 坐标
#buttons 按钮 0未按下 1左键 2右键
#clicks 点击次数
#delta 滚轮值
def onViewMouseMove(view, mp, buttons, clicks, delta):
	firstTouch = FALSE
	secondTouch = FALSE
	firstPoint = mp
	secondPoint = mp
	if (buttons == 1):
		firstTouch = TRUE
	if (view.m_type == "grid"):
		mouseMoveGrid(view, firstTouch, secondTouch, firstPoint, secondPoint)
		invalidateView(view, view.m_paint)
	elif (view.m_type == "tree"):
		mouseMoveTree(view, firstTouch, secondTouch, firstPoint, secondPoint)
	elif(view.m_type == "chart"):
		mouseMoveChart(view, firstTouch, secondTouch, firstPoint, secondPoint)
		invalidateView(view, view.m_paint)
	elif(view.m_type == "div" or view.m_type =="layout"):
		mouseMoveDiv(view, firstTouch, secondTouch, firstPoint, secondPoint)
		invalidateView(view, view.m_paint)
	elif(view.m_type == "button"):
		invalidateView(view, view.m_paint)
		
#视图的鼠标按下方法
#view 视图
#mp 坐标
#buttons 按钮 0未按下 1左键 2右键
#clicks 点击次数
#delta 滚轮值
def onViewMouseDown(view, mp, buttons, clicks, delta):
	firstTouch = FALSE
	secondTouch = FALSE
	firstPoint = mp
	secondPoint = mp
	if (buttons == 1):
		firstTouch = TRUE
	if (view.m_type == "grid"):
		mouseDownGrid(view, firstTouch, secondTouch, firstPoint, secondPoint)
		invalidateView(view, view.m_paint)
	elif (view.m_type == "tree"):
		mouseDownTree(view, firstTouch, secondTouch, firstPoint, secondPoint)
		invalidateView(view, view.m_paint)
	elif(view.m_type == "chart"):
		view.m_selectShape = ""
		view.m_selectShapeEx = ""
		facecat.m_mouseDownPoint_Chart = mp;
		if (view.m_sPlot == None):
			selectShape(view, mp)
	elif(view.m_type == "div" or view.m_type =="layout"):
		mouseDownDiv(view, firstTouch, secondTouch, firstPoint, secondPoint)
		invalidateView(view, view.m_paint)
	elif(view.m_type == "button"):
		invalidateView(view, view.m_paint)

#视图的鼠标进入方法
#view 视图
#mp 坐标
#buttons 按钮 0未按下 1左键 2右键
#clicks 点击次数
#delta 滚轮值
def onViewMouseEnter(view, mp, buttons, clicks, delta):
	firstTouch = FALSE
	secondTouch = FALSE
	firstPoint = mp
	secondPoint = mp
	if (buttons == 1):
		firstTouch = TRUE

#视图的鼠标进入方法
#view 视图
#mp 坐标
#buttons 按钮 0未按下 1左键 2右键
#clicks 点击次数
#delta 滚轮值
def onViewMouseLeave(view, mp, buttons, clicks, delta):
	firstTouch = FALSE
	secondTouch = FALSE
	firstPoint = mp
	secondPoint = mp
	if (buttons == 1):
		firstTouch = TRUE
	if(view.m_type == "button"):
		invalidateView(view, view.m_paint)

#视图的鼠标抬起方法
#view 视图
#mp 坐标
#buttons 按钮 0未按下 1左键 2右键
#clicks 点击次数
#delta 滚轮值
def onViewMouseUp(view, mp, buttons, clicks, delta):
	firstTouch = FALSE
	secondTouch = FALSE
	firstPoint = mp
	secondPoint = mp
	if (buttons == 1):
		firstTouch = TRUE
	if (view.m_type == "grid"):
		mouseUpGrid(view, firstTouch, secondTouch, firstPoint, secondPoint)
		invalidateView(view, view.m_paint)
	elif (view.m_type == "tree"):
		mouseUpTree(view, firstTouch, secondTouch, firstPoint, secondPoint)
		invalidateView(view, view.m_paint)
	elif (view.m_type == "div" or view.m_type =="layout"):
		mouseUpDiv(view, firstTouch, secondTouch, firstPoint, secondPoint)
		invalidateView(view, view.m_paint)
	elif(view.m_type == "chart"):
		facecat.m_firstTouchIndexCache_Chart = -1
		facecat.m_secondTouchIndexCache_Chart = -1
		invalidateView(view, view.m_paint)
	elif(view.m_type == "button"):
		invalidateView(view, view.m_paint)

#视图的鼠标点击方法
#view 视图
#mp 坐标
#buttons 按钮 0未按下 1左键 2右键
#clicks 点击次数
#delta 滚轮值
def onViewClick(view, mp, buttons, clicks, delta):
	global m_paint
	global ctp
	if(view.m_type == "radiobutton"):
		clickRadioButton(view, mp)
		if(view.m_parent != None):
			invalidateView(view.m_parent, view.m_parent.m_paint)
		else:
			invalidateView(view, view.m_paint)
	elif(view.m_type == "checkbox"):
		clickCheckBox(view, mp)
		invalidateView(view, view.m_paint)
	elif(view.m_type == "tabbutton"):
		tabView = view.m_parent
		for i in range(0, len(tabView.m_tabPages)):
			if(tabView.m_tabPages[i].m_headerButton == view):
				selectTabPage(tabView, tabView.m_tabPages[i])
		invalidateView(tabView, tabView.m_paint)
	elif(view.m_name == "btnOrder"):
		txtIssueCode = findViewByName("txtIssueCode", m_paint.m_views)
		spinVolume = findViewByName("spinVolume", m_paint.m_views)
		spinPrice = findViewByName("spinPrice", m_paint.m_views)
		rbBuy = findViewByName("rbBuy", m_paint.m_views)
		rbSell = findViewByName("rbSell", m_paint.m_views)
		rbOpen = findViewByName("rbOpen", m_paint.m_views)
		rbCloseToday = findViewByName("rbCloseToday", m_paint.m_views)
		rbClose = findViewByName("rbClose", m_paint.m_views)
		issueCode = getViewAttribute(txtIssueCode, "text")
		if(issueCode in m_allCodes):
			exchangeID = m_allCodes[issueCode].exchangeID
			volume = int(getViewAttribute(spinVolume, "text"))
			price = float(getViewAttribute(spinPrice, "text"))
			if(rbBuy.m_checked):
				if(rbOpen.m_checked):
					ctp.bidOpen(ctp.generateReqID(), issueCode, exchangeID, price, volume, 51, "")
				elif(rbCloseToday.m_checked):
					ctp.bidCloseToday(ctp.generateReqID(), issueCode, exchangeID, price, volume, 51, "")
				elif(rbClose.m_checked):
					ctp.bidClose(ctp.generateReqID(), issueCode, exchangeID, price, volume, 51, "")
			else:
				if(rbOpen.m_checked):
					ctp.askOpen(ctp.generateReqID(), issueCode, exchangeID, price, volume, 51, "")
				elif(rbCloseToday.m_checked):
					ctp.askCloseToday(ctp.generateReqID(), issueCode, exchangeID, price, volume, 51, "")
				elif(rbClose.m_checked):
					ctp.askClose(ctp.generateReqID(), issueCode, exchangeID, price, volume, 51, "")
	elif(view.m_name == "btnCancelOrder2"):
		gridOrder = findViewByName("gridOrder", m_paint.m_views)
		for i in range(0, len(gridOrder.m_rows)):
			row = gridOrder.m_rows[i]
			if(row.m_selected):
				orderSysID = row.m_cells[0].m_value
				exchangeID = row.m_cells[16].m_value
				ctp.cancelOrder(ctp.generateReqID(), exchangeID, orderSysID, "")
				break
				
	if(view.m_name == "cbInvestorPosition"):
		gridInvestorPosition = findViewByName("gridInvestorPosition", m_paint.m_views)
		gridInvestorPositionDetail = findViewByName("gridInvestorPositionDetail", m_paint.m_views) 
		gridInvestorPosition.m_visible = TRUE
		gridInvestorPositionDetail.m_visible = FALSE
		invalidateView(gridInvestorPosition, gridInvestorPosition.m_paint)
	elif(view.m_name == "cbInvestorPositionDetail"):
		gridInvestorPosition = findViewByName("gridInvestorPosition", m_paint.m_views)
		gridInvestorPositionDetail = findViewByName("gridInvestorPositionDetail", m_paint.m_views) 
		gridInvestorPosition.m_visible = FALSE
		gridInvestorPositionDetail.m_visible = TRUE
		invalidateView(gridInvestorPositionDetail, gridInvestorPositionDetail.m_paint)
		

#视图的鼠标滚动方法
#view 视图
#mp 坐标
#buttons 按钮 0未按下 1左键 2右键
#clicks 点击次数
#delta 滚轮值
def onViewMouseWheel(view, mp, buttons, clicks, delta):
	if (view.m_type == "grid"):
		mouseWheelGrid(view, delta)
		invalidateView(view, view.m_paint)
	elif (view.m_type == "tree"):
		mouseWheelTree(view, delta)
		invalidateView(view, view.m_paint)
	elif (view.m_type == "div" or view.m_type =="layout"):
		mouseWheelDiv(view, delta)
		invalidateView(view, view.m_paint)
	elif(view.m_type == "chart"):
		if(delta > 0):
			zoomOutChart(view);
		elif(delta < 0):
			zoomInChart(view);
		invalidateView(view, view.m_paint)

m_xml = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\r\n<html xmlns=\"facecat\">\r\n  <head>\r\n  </head>\r\n  <body>\r\n    <div type=\"splitlayout\" name=\"divAll\" candragsplitter=\"true\" layoutstyle=\"toptobottom\" dock=\"fill\" size=\"400,505\" splitterposition=\"0,80,400,80\" bordercolor=\"none\">\r\n      <div type=\"tab\" name=\"tabTradeAccount\" bordercolor=\"none\" backcolor=\"none\">\r\n        <div type=\"tabpage\" name=\"pageTradeAccount\" text=\"持仓\" headersize=\"100,0\" backcolor=\"none\" bordercolor=\"none\" padding=\"5,5,5,5\">\r\n          <table name=\"gridTradeAccount\" dock=\"fill\" headerheight=\"70\" showhscrollbar=\"false\" bordercolor=\"none\" backcolor=\"-200000000163\">\r\n            <tr>\r\n              <th name=\"colF1\" text=\"静态权益\" width=\"120\" location=\"0,0\" size=\"120,70\" />\r\n              <th name=\"colF2\" text=\"平仓盈亏\" width=\"120\" />\r\n              <th name=\"colF3\" text=\"浮动盈亏\" width=\"120\" />\r\n              <th name=\"colF4\" text=\"持仓盈亏\" width=\"120\" location=\"240,0\" size=\"120,70\" />\r\n              <th name=\"colF5\" text=\"动态权益\" width=\"120\" />\r\n              <th name=\"colF6\" text=\"占用保证金\" width=\"120\" />\r\n              <th name=\"colF7\" text=\"下单冻结\" width=\"120\" />\r\n              <th name=\"colF8\" text=\"可用资金\" width=\"120\" />\r\n              <th name=\"colF9\" text=\"风险度\" width=\"120\" />\r\n              <th name=\"colF10\" text=\"冻结保证金\" width=\"120\" />\r\n              <th name=\"colF11\" text=\"冻结手续费\" width=\"120\" />\r\n              <th name=\"colF12\" text=\"手续费\" width=\"120\" />\r\n              <th name=\"colF13\" text=\"上次结算准备金\" width=\"120\" />\r\n              <th name=\"colF14\" text=\"上次信用额度\" width=\"120\" />\r\n              <th name=\"colF15\" text=\"上次质押金额\" width=\"120\" />\r\n              <th name=\"colF16\" text=\"质押金额\" width=\"120\" />\r\n              <th name=\"colF17\" text=\"今日出金\" width=\"120\" />\r\n              <th name=\"colF18\" text=\"今日入金\" width=\"120\" />\r\n              <th name=\"colF19\" text=\"信用金额\" width=\"120\" />\r\n              <th name=\"colF20\" text=\"保底资金\" width=\"120\" />\r\n              <th name=\"colF21\" text=\"可取资金\" width=\"120\" />\r\n            </tr>\r\n          </table>\r\n        </div>\r\n      </div>\r\n      <div type=\"splitlayout\" name=\"divBottom\" candragsplitter=\"true\" layoutstyle=\"bottomtotop\" size=\"400,450\" splitterposition=\"0,430,400,430\" bordercolor=\"none\" backcolor=\"none\">\r\n        <div name=\"divStatus\" size=\"966,17\">\r\n          <label name=\"lblTradingTime\" text=\"--\" location=\"3,2\" size=\"100,20\" font=\"Default,12\" />\r\n          <label name=\"lbllog\" text=\"--\" location=\"105,2\" size=\"352,20\" font=\"Default,12\" />\r\n        </div>\r\n        <div type=\"splitlayout\" name=\"divMiddle\" candragsplitter=\"true\" layoutstyle=\"toptobottom\" size=\"600,600\" splitmode=\"percentsize\" splitterposition=\"0,450,400,450\" bordercolor=\"none\" backcolor=\"none\">\r\n          <div type=\"splitlayout\" name=\"divMiddleTop\" candragsplitter=\"true\" layoutstyle=\"bottomtotop\" size=\"600,600\" splitterposition=\"0,330,400,330\" bordercolor=\"none\" backcolor=\"none\">\r\n            <div bordercolor=\"none\" padding=\"5,5,5,5\" backcolor=\"none\">\r\n              <div type=\"splitlayout\" name=\"divMain\" dock=\"fill\" candragsplitter=\"true\" layoutstyle=\"lefttoright\" size=\"420,420\" splitterposition=\"310,0,310,300\" bordercolor=\"none\" backcolor=\"none\">\r\n                <div bordercolor=\"none\" backcolor=\"none\" padding=\"0,0,5,0\">\r\n                  <div type=\"tab\" name=\"tabTradeMain\" selectedindex=\"0\" location=\"0,0\" size=\"1166,270\" dock=\"fill\" bordercolor=\"rgb(100,100,100)\" backcolor=\"-200000000163\">\r\n                    <div type=\"tabpage\" name=\"pageTrade\" text=\"标准下单\" backcolor=\"none\" bordercolor=\"none\">\r\n                      <div name=\"divTrade\" size=\"310,250\" dock=\"fill\" location=\"0,0\" backcolor=\"Back\">\r\n                        <label name=\"lblContract\" text=\"合约\" location=\"8,18\" size=\"37,20\" font=\"Default,14\" />\r\n                        <label name=\"lblBuySell\" text=\"买卖\" location=\"8,49\" size=\"38,19\" font=\"Default,14\" />\r\n                        <input type=\"custom\" cid=\"ribbonbutton2\" name=\"btnOpenCloseMode\" text=\"自动\" location=\"3,76\" size=\"46,20\" />\r\n                        <label name=\"lblVolume\" text=\"手数\" location=\"8,109\" size=\"38,19\" font=\"Default,14\" />\r\n                        <input type=\"radio\" name=\"rbOpen\" backcolor=\"rgba(43,138,195,100)\" checked=\"true\" text=\"开仓\" location=\"52,76\" size=\"65,20\" groupname=\"OpenClose\" />\r\n                        <input type=\"radio\" name=\"rbCloseToday\" text=\"平今\" location=\"120,76\" size=\"65,20\" groupname=\"OpenClose\" />\r\n                        <input type=\"radio\" name=\"rbClose\" text=\"平仓\" location=\"182,76\" size=\"65,20\" groupname=\"OpenClose\" />\r\n                        <input type=\"radio\" name=\"rbBuy\" backcolor=\"rgba(255,0,0,100)\" checked=\"true\" text=\"买入\" location=\"53,47\" size=\"64,20\" groupname=\"BuySell\" />\r\n                        <input type=\"radio\" name=\"rbSell\" text=\"卖出\" location=\"119,47\" size=\"64,20\" groupname=\"BuySell\" />\r\n                        <input type=\"text\" name=\"txtIssueCode\" font=\"Default,20\" location=\"53,11\" size=\"163,28\" lineheight=\"28\" multiline=\"false\" />\r\n                        <input type=\"checkbox\" name=\"cbLock\" text=\"锁定\" location=\"220,15\" size=\"73,20\" canfocus=\"false\" buttonsize=\"16,16\" />\r\n                        <input type=\"range\" name=\"spinVolume\" font=\"Default,20\" digit=\"0\" location=\"52,102\" size=\"115,28\" lineheight=\"28\" maximum=\"100000000\" minimum=\"1\" textalign=\"far\" />\r\n                        <input type=\"range\" name=\"spinPrice\" digit=\"2\" font=\"Default,20\" location=\"52,142\" size=\"115,24\" lineheight=\"28\" maximum=\"100000000\" textalign=\"far\" />\r\n                        <input type=\"custom\" cid=\"ribbonbutton2\" name=\"btnOrder\" font=\"Default,16\" text=\"下单\" backcolor=\"rgb(15,193,118)\" location=\"8,179\" size=\"211,48\" />\r\n                        <input type=\"custom\" cid=\"ribbonbutton2\" name=\"btnCancel\" text=\"取消\" location=\"226,184\" backcolor=\"rgb(248,73,96)\" size=\"74,24\" font=\"Default,12\" />\r\n                        <input type=\"custom\" cid=\"ribbonbutton2\" name=\"btnPreCondition\" text=\"预埋/条件\" location=\"226,209\" size=\"74,23\" font=\"Default,12\" />\r\n                        <label name=\"lblLess\" text=\"&lt;=\" location=\"185,104\" size=\"26,21\" font=\"Default,16\" />\r\n                        <label name=\"lblMaxVolume\" text=\"0\" location=\"206,104\" size=\"16,21\" font=\"Default,16\" />\r\n                        <label name=\"lblUp\" text=\"0\" location=\"188,121\" size=\"100,20\" opacity=\"1\" />\r\n                        <label name=\"lblAskPrice\" text=\"0\" location=\"188,135\" size=\"53,20\" />\r\n                        <label name=\"lblBidPrice\" text=\"0\" location=\"188,149\" size=\"51,21\" />\r\n                        <label name=\"lblDown\" text=\"0\" location=\"188,163\" size=\"48,20\" />\r\n                        <label name=\"Label\" text=\"/\" location=\"241,136\" size=\"17,20\" font=\"Default,12\" />\r\n                        <label name=\"Label1\" text=\"/\" location=\"239,150\" size=\"16,20\" font=\"Default,12\" />\r\n                        <label name=\"lblAskVolume\" text=\"0\" location=\"250,136\" size=\"57,18\" />\r\n                        <label name=\"lblBidVolume\" text=\"0\" location=\"250,150\" size=\"57,20\" />\r\n                        <input type=\"custom\" cid=\"ribbonbutton2\" name=\"btnTradeMode\" text=\"跟盘\" location=\"3,143\" size=\"46,20\" />\r\n                      </div>\r\n                    </div>\r\n                  </div>\r\n                </div>\r\n                <div type=\"splitlayout\" name=\"divMain\" dock=\"fill\" candragsplitter=\"true\" layoutstyle=\"righttoleft\" size=\"420,420\" splitterposition=\"100,0\" bordercolor=\"none\" backcolor=\"none\">\r\n                  <div bordercolor=\"none\" backcolor=\"none\" padding=\"5,0,0,0\">\r\n                    <div type=\"tab\" name=\"tabOrder2\" selectedindex=\"1\" backcolor=\"-200000000163\" bordercolor=\"rgb(100,100,100)\" dock=\"fill\">\r\n                      <div type=\"tabpage\" name=\"pageChart\" text=\"图形\" bordercolor=\"none\" backcolor=\"none\">\r\n                        <chart name=\"chart\" dock=\"fill\" />\r\n                      </div>\r\n                    </div>\r\n                  </div>\r\n                  <div type=\"tab\" name=\"tabOrder\" selectedindex=\"1\" backcolor=\"-200000000163\" bordercolor=\"rgb(100,100,100)\">\r\n                    <div type=\"tabpage\" name=\"pageAllOrders\" text=\"所有委托单\" backcolor=\"none\" bordercolor=\"none\">\r\n                      <div type=\"splitlayout\" name=\"divOrder\" dock=\"fill\" layoutstyle=\"bottomtotop\" size=\"400,400\" splitterposition=\"0,370,400,370\" backcolor=\"none\" bordercolor=\"none\">\r\n                        <div name=\"divDealRecordType\" backcolor=\"none\" bordercolor=\"none\">\r\n                          <input type=\"radio\" name=\"rdAllOrders\" groupname=\"allOrders\" checked=\"true\" location=\"0,6\" text=\"全部单\" size=\"100,20\" />\r\n                          <input type=\"radio\" name=\"rdOrder\" groupname=\"allOrders\" location=\"100,6\" text=\"挂单\" size=\"100,20\" />\r\n                          <input type=\"radio\" name=\"rdDeal\" groupname=\"allOrders\" location=\"200,6\" text=\"已成交\" size=\"100,20\" />\r\n                          <input type=\"radio\" name=\"rdCancel\" groupname=\"allOrders\" location=\"300,6\" text=\"已撤单/错单\" size=\"120,20\" />\r\n                          <input type=\"custom\" cid=\"ribbonbutton2\" name=\"btnCancelOrder2\" location=\"450,2\" size=\"100,26\" text=\"撤单\" />\r\n                          <input type=\"custom\" cid=\"ribbonbutton2\" name=\"btnCancelAllOrder2\" location=\"570,2\" size=\"100,26\" text=\"全撤\" />\r\n                        </div>\r\n                        <table name=\"gridOrder\" dock=\"Fill\" size=\"569,330\" backcolor=\"none\" bordercolor=\"none\">\r\n                          <tr>\r\n                            <th name=\"colA1\" columntype=\"text\" text=\"报单编号\" width=\"80\" />\r\n                            <th name=\"colA2\" columntype=\"text\" text=\"合约\" width=\"80\" />\r\n                            <th name=\"colA3\" columntype=\"text\" horizontalalign=\"center\" text=\"买卖\" width=\"60\" />\r\n                            <th name=\"colA4\" columntype=\"text\" horizontalalign=\"center\" text=\"开平\" width=\"60\" />\r\n                            <th name=\"colA5\" columntype=\"text\" horizontalalign=\"center\" text=\"挂单状态\" width=\"140\" />\r\n                            <th name=\"colA6\" columntype=\"double\" horizontalalign=\"far\" text=\"报单价格\" width=\"80\" />\r\n                            <th name=\"colA7\" columntype=\"int\" horizontalalign=\"far\" text=\"报单手数\" width=\"80\" />\r\n                            <th name=\"colA8\" columntype=\"int\" horizontalalign=\"far\" text=\"未成交手数\" width=\"80\" />\r\n                            <th name=\"colA9\" columntype=\"int\" horizontalalign=\"far\" text=\"成交手数\" width=\"80\" />\r\n                            <th name=\"colA10\" columntype=\"text\" horizontalalign=\"center\" text=\"报单时间\" width=\"60\" />\r\n                            <th name=\"colA11\" columntype=\"text\" horizontalalign=\"center\" text=\"最后成交时间\" width=\"80\" />\r\n                            <th name=\"colA12\" columntype=\"double\" horizontalalign=\"far\" text=\"成交均价\" width=\"80\" />\r\n                            <th name=\"colA13\" columntype=\"double\" horizontalalign=\"far\" text=\"冻结保证金\" width=\"80\" />\r\n                            <th name=\"colA14\" columntype=\"double\" horizontalalign=\"far\" text=\"冻结手续费\" width=\"80\" />\r\n                            <th name=\"colA15\" columntype=\"text\" horizontalalign=\"center\" text=\"投保\" width=\"60\" />\r\n                            <th name=\"colA16\" columntype=\"text\" text=\"交易所\" width=\"80\" />\r\n                            <th name=\"colA18\" columntype=\"text\" horizontalalign=\"center\" text=\"报单价格条件\" width=\"100\" />\r\n                            <th name=\"colA19\" columntype=\"text\" text=\"有效期类型\" width=\"200\" />\r\n                            <th name=\"colA20\" columntype=\"text\" horizontalalign=\"center\" text=\"报单类型\" width=\"60\" />\r\n                            <th name=\"colA21\" columntype=\"text\" horizontalalign=\"center\" text=\"是否强平\" width=\"80\" />\r\n                            <th name=\"colA22\" columntype=\"text\" horizontalalign=\"center\" text=\"强平原因\" width=\"80\" />\r\n                            <th name=\"colA23\" columntype=\"text\" text=\"指令结果\" width=\"80\" />\r\n                            <th name=\"colA24\" columntype=\"text\" text=\"客户端信息\" width=\"80\" />\r\n                            <th name=\"colA25\" columntype=\"text\" text=\"撤单锁定\" width=\"60\" />\r\n                          </tr>\r\n                        </table>\r\n                      </div>\r\n                    </div>\r\n                    <div type=\"tabpage\" name=\"pageTradeRecord\" text=\"成交记录\" backcolor=\"none\" bordercolor=\"none\">\r\n                      <div type=\"splitlayout\" name=\"divTradeRecord\" dock=\"fill\" layoutstyle=\"bottomtotop\" size=\"400,400\" splitterposition=\"0,370,400,370\" backcolor=\"none\" bordercolor=\"none\">\r\n                        <div name=\"divTradeRecordType\" backcolor=\"none\" bordercolor=\"none\">\r\n                          <input type=\"radio\" name=\"rdDetail\" groupname=\"tradeRecordType\" checked=\"true\" location=\"0,5\" text=\"明细\" size=\"100,20\" />\r\n                          <input type=\"radio\" name=\"rdSummary\" groupname=\"tradeRecordType\" location=\"100,5\" text=\"合计\" size=\"100,20\" />\r\n                        </div>\r\n                        <div name=\"divTradeRecordInner\" backcolor=\"none\" bordercolor=\"none\">\r\n                          <table name=\"gridTradeRecord\" dock=\"fill\" backcolor=\"none\" bordercolor=\"none\">\r\n                            <tr>\r\n                              <th name=\"colR1\" columntype=\"text\" text=\"成交编号\" width=\"80\" />\r\n                              <th name=\"colR2\" columntype=\"text\" text=\"合约\" width=\"80\" />\r\n                              <th name=\"colR3\" columntype=\"text\" horizontalalign=\"center\" text=\"买卖\" width=\"60\" />\r\n                              <th name=\"colR4\" columntype=\"text\" horizontalalign=\"center\" text=\"开平\" width=\"60\" />\r\n                              <th name=\"colR5\" columntype=\"double\" horizontalalign=\"far\" text=\"成交价格\" width=\"80\" />\r\n                              <th name=\"colR6\" columntype=\"int\" horizontalalign=\"far\" text=\"成交手数\" width=\"80\" />\r\n                              <th name=\"colR7\" columntype=\"text\" horizontalalign=\"center\" text=\"成交时间\" width=\"80\" />\r\n                              <th name=\"colR8\" columntype=\"text\" horizontalalign=\"center\" text=\"报单编号\" width=\"80\" />\r\n                              <th name=\"colR9\" columntype=\"text\" horizontalalign=\"center\" text=\"成交类型\" width=\"80\" />\r\n                              <th name=\"colR10\" columntype=\"text\" horizontalalign=\"center\" text=\"投保\" width=\"60\" />\r\n                              <th name=\"colR11\" columntype=\"text\" text=\"交易所\" width=\"80\" />\r\n                              <th name=\"colR12\" columntype=\"double\" horizontalalign=\"far\" text=\"手续费\" width=\"80\" />\r\n                            </tr>\r\n                          </table>\r\n                          <table name=\"gridTradeStatistics\" dock=\"fill\" visible=\"false\" backcolor=\"none\" bordercolor=\"none\">\r\n                            <tr>\r\n                              <th name=\"colS1\" columntype=\"text\" text=\"合约\" width=\"80\" />\r\n                              <th name=\"colS2\" columntype=\"text\" text=\"交易所\" width=\"80\" />\r\n                              <th name=\"colS3\" columntype=\"text\" horizontalalign=\"center\" text=\"买卖\" width=\"80\" />\r\n                              <th name=\"colS4\" columntype=\"text\" horizontalalign=\"center\" text=\"开平\" width=\"80\" />\r\n                              <th name=\"colS5\" columntype=\"double\" horizontalalign=\"far\" text=\"成交均价\" width=\"100\" />\r\n                              <th name=\"colS6\" columntype=\"int\" horizontalalign=\"far\" text=\"成交手数\" width=\"100\" />\r\n                              <th name=\"colS7\" columntype=\"double\" horizontalalign=\"far\" text=\"手续费\" width=\"100\" />\r\n                              <th name=\"colS8\" columntype=\"text\" horizontalalign=\"center\" text=\"投保\" width=\"60\" />\r\n                            </tr>\r\n                          </table>\r\n                        </div>\r\n                      </div>\r\n                    </div>\r\n                  </div>\r\n                </div>\r\n              </div>\r\n            </div>\r\n            <div bordercolor=\"none\" backcolor=\"none\" padding=\"5,5,5,5\">\r\n              <div type=\"tab\" name=\"tabQuote\" selectedindex=\"0\" size=\"400,400\" backcolor=\"-200000000163\" dock=\"fill\" bordercolor=\"rgb(100,100,100)\">\r\n                <div type=\"tabpage\" name=\"pagePageQuote\" text=\"报价表\" bordercolor=\"none\" backcolor=\"none\">\r\n                  <table name=\"gridLatestData\" dock=\"fill\" location=\"0,0\" size=\"914,160\" bordercolor=\"none\" backcolor=\"none\">\r\n                    <tr>\r\n                      <th name=\"colQ1\" columntype=\"text\" text=\"合约\" width=\"80\" />\r\n                      <th name=\"colQ2\" columntype=\"text\" text=\"合约名\" width=\"100\" />\r\n                      <th name=\"colQ3\" columntype=\"double\" horizontalalign=\"far\" text=\"最新价\" width=\"60\" />\r\n                      <th name=\"colQ4\" columntype=\"double\" horizontalalign=\"far\" text=\"涨跌\" width=\"60\" />\r\n                      <th name=\"colQ5\" columntype=\"double\" horizontalalign=\"far\" text=\"买价\" width=\"60\" location=\"300,0\" size=\"60,20\" />\r\n                      <th name=\"colQ6\" columntype=\"int\" horizontalalign=\"far\" text=\"买量\" width=\"60\" location=\"360,0\" size=\"60,20\" />\r\n                      <th name=\"colQ7\" columntype=\"double\" horizontalalign=\"far\" text=\"卖价\" width=\"60\" />\r\n                      <th name=\"colQ8\" columntype=\"int\" horizontalalign=\"far\" text=\"卖量\" width=\"60\" />\r\n                      <th name=\"colQ9\" columntype=\"int\" horizontalalign=\"far\" text=\"成交量\" width=\"60\" />\r\n                      <th name=\"colQ10\" columntype=\"int\" horizontalalign=\"far\" text=\"持仓量\" width=\"60\" />\r\n                      <th name=\"colQ11\" columntype=\"double\" horizontalalign=\"far\" text=\"涨停价\" width=\"60\" />\r\n                      <th name=\"colQ12\" columntype=\"double\" horizontalalign=\"far\" text=\"涨停价\" width=\"60\" />\r\n                      <th name=\"colQ13\" columntype=\"double\" horizontalalign=\"far\" text=\"今开盘\" width=\"60\" />\r\n                      <th name=\"colQ14\" columntype=\"double\" horizontalalign=\"far\" text=\"昨结算\" width=\"60\" />\r\n                      <th name=\"colQ15\" columntype=\"double\" horizontalalign=\"far\" text=\"最高价\" width=\"60\" />\r\n                      <th name=\"colQ16\" columntype=\"double\" horizontalalign=\"far\" text=\"最低价\" width=\"60\" />\r\n                      <th name=\"colQ17\" columntype=\"int\" horizontalalign=\"far\" text=\"现量\" width=\"60\" />\r\n                      <th name=\"colQ18\" columntype=\"percent\" horizontalalign=\"far\" text=\"涨跌幅\" width=\"60\" />\r\n                      <th name=\"colQ19\" columntype=\"double\" horizontalalign=\"far\" text=\"昨收盘\" width=\"60\" />\r\n                      <th name=\"colQ20\" columntype=\"thousands\" horizontalalign=\"far\" text=\"成交额\" width=\"100\" />\r\n                      <th name=\"colQ21\" columntype=\"text\" text=\"交易所\" width=\"60\" />\r\n                      <th name=\"colQ22\" columntype=\"text\" horizontalalign=\"center\" text=\"行情更新时间\" width=\"100\" />\r\n                      <th name=\"colQ23\" columntype=\"double\" text=\"昨持仓量\" width=\"60\" />\r\n                      <th name=\"colQ24\" columntype=\"double\" text=\"今收盘\" width=\"60\" />\r\n                      <th name=\"colQ25\" columntype=\"double\" text=\"结算价\" width=\"60\" />\r\n                      <th name=\"colQ26\" columntype=\"double\" text=\"当日均价\" width=\"80\" />\r\n                      <th name=\"colQ27\" columntype=\"int\" text=\"持仓增减\" width=\"80\" />\r\n                      <th name=\"colQ28\" columntype=\"double\" text=\"组合买价\" width=\"80\" />\r\n                      <th name=\"colQ29\" columntype=\"int\" text=\"组合买量\" width=\"80\" />\r\n                      <th name=\"colQ30\" columntype=\"double\" text=\"组合卖价\" width=\"80\" />\r\n                      <th name=\"colQ31\" columntype=\"int\" text=\"组合卖量\" width=\"80\" />\r\n                      <th name=\"colQ32\" columntype=\"int\" text=\"撤单次数\" width=\"80\" />\r\n                    </tr>\r\n                  </table>\r\n                </div>\r\n                <div type=\"tabpage\" name=\"pageContracts\" text=\"合约列表\" bordercolor=\"none\" backcolor=\"none\">\r\n                  <table name=\"gridContracts\" dock=\"fill\" bordercolor=\"none\" backcolor=\"none\">\r\n                    <tr>\r\n                      <th name=\"colC1\" columntype=\"text\" text=\"品种代码\" width=\"80\" />\r\n                      <th name=\"colC2\" columntype=\"text\" text=\"合约\" width=\"60\" />\r\n                      <th name=\"colC3\" columntype=\"text\" text=\"合约名\" width=\"100\" />\r\n                      <th name=\"colC4\" columntype=\"text\" text=\"交易所\" width=\"60\" />\r\n                      <th name=\"colC5\" columntype=\"int\" horizontalalign=\"far\" text=\"合约乘数\" width=\"100\" />\r\n                      <th name=\"colC6\" columntype=\"double\" horizontalalign=\"far\" text=\"最小价格变动单位\" width=\"100\" />\r\n                      <th name=\"colC7\" columntype=\"text\" horizontalalign=\"center\" text=\"品种类型\" width=\"100\" />\r\n                      <th name=\"colC8\" columntype=\"text\" horizontalalign=\"center\" text=\"最后日期\" width=\"100\" />\r\n                      <th name=\"colC9\" columntype=\"percent\" horizontalalign=\"far\" text=\"多头保证金率\" width=\"100\" />\r\n                      <th name=\"colC10\" columntype=\"percent\" horizontalalign=\"far\" text=\"空头保证金率\" width=\"100\" />\r\n                      <th name=\"colC11\" columntype=\"double\" horizontalalign=\"far\" text=\"开仓手续费\" width=\"100\" />\r\n                      <th name=\"colC12\" columntype=\"double\" horizontalalign=\"far\" text=\"平仓手续费\" width=\"100\" />\r\n                      <th name=\"colC13\" columntype=\"double\" horizontalalign=\"far\" text=\"平今手续费\" width=\"100\" />\r\n                      <th name=\"colC14\" columntype=\"percent\" horizontalalign=\"far\" text=\"开仓手续费率\" width=\"100\" />\r\n                      <th name=\"colC15\" columntype=\"percent\" horizontalalign=\"far\" text=\"平仓手续费率\" width=\"100\" />\r\n                      <th name=\"colC16\" columntype=\"percent\" horizontalalign=\"far\" text=\"平今手续费率\" width=\"100\" />\r\n                      <th name=\"colC17\" columntype=\"int\" horizontalalign=\"far\" text=\"市价单最大下单量\" width=\"100\" />\r\n                      <th name=\"colC18\" columntype=\"int\" horizontalalign=\"far\" text=\"限价单最大下单量\" width=\"100\" />\r\n                    </tr>\r\n                  </table>\r\n                </div>\r\n              </div>\r\n            </div>\r\n          </div>\r\n          <div bordercolor=\"none\" padding=\"5,5,5,5\" backcolor=\"-200000000163\">\r\n            <div type=\"tab\" name=\"tabInvestorPosition\" selectedindex=\"0\" dock=\"fill\" bordercolor=\"rgb(100,100,100)\" backcolor=\"none\">\r\n              <div type=\"tabpage\" name=\"pagePageInvestorPosition\" text=\"持仓\" bordercolor=\"none\" backcolor=\"none\">\r\n                <div type=\"splitlayout\" name=\"divInvestorPosition\" dock=\"fill\" layoutstyle=\"bottomtotop\" size=\"400,400\" splitterposition=\"0,370,400,370\" bordercolor=\"none\" backcolor=\"none\">\r\n                  <div name=\"divInvestorPositionBottom\" bordercolor=\"none\" backcolor=\"none\">\r\n                    <input type=\"radio\" name=\"cbInvestorPosition\" checked=\"true\" location=\"5,5\" groupname=\"InvestorPosition\" size=\"90,20\" text=\"持仓\" />\r\n                    <input type=\"radio\" name=\"cbInvestorPositionDetail\" groupname=\"InvestorPosition\" location=\"100,5\" size=\"100,20\" text=\"持仓明细\" />\r\n                    <input type=\"radio\" name=\"cbCompPosition\" groupname=\"InvestorPosition\" location=\"180,3\" size=\"80,23\" text=\"组合持仓\" visible=\"false\" />\r\n                    <input type=\"custom\" cid=\"ribbonbutton2\" name=\"btnOpenInterestIP\" location=\"300,3\" size=\"80,23\" text=\"对价平仓\" height=\"24\" />\r\n                    <input type=\"custom\" cid=\"ribbonbutton2\" name=\"btnMarketPositionIP\" location=\"390,3\" size=\"80,23\" text=\"市价平仓\" height=\"24\" />\r\n                    <input type=\"custom\" cid=\"ribbonbutton2\" name=\"btnMarketBackhandIP\" location=\"480,3\" size=\"80,23\" text=\"市价反手\" height=\"24\" />\r\n                  </div>\r\n                  <div name=\"divInvestorPositionTop\" bordercolor=\"none\" backcolor=\"none\">\r\n                    <table name=\"gridInvestorPosition\" dock=\"fill\" bordercolor=\"none\" backcolor=\"none\">\r\n                      <tr>\r\n                        <th name=\"colP1\" columntype=\"text\" text=\"合约\" width=\"80\" />\r\n                        <th name=\"colP2\" columntype=\"text\" horizontalalign=\"center\" text=\"多空\" width=\"60\" />\r\n                        <th name=\"colP3\" columntype=\"int\" horizontalalign=\"far\" text=\"总持仓\" width=\"60\" />\r\n                        <th name=\"colP4\" columntype=\"int\" horizontalalign=\"far\" text=\"昨仓\" width=\"60\" />\r\n                        <th name=\"colP5\" columntype=\"int\" horizontalalign=\"far\" text=\"今仓\" width=\"60\" />\r\n                        <th name=\"colP6\" columntype=\"int\" horizontalalign=\"far\" text=\"可平量\" width=\"60\" />\r\n                        <th name=\"colP7\" columntype=\"double\" horizontalalign=\"far\" text=\"持仓均价\" width=\"80\" />\r\n                        <th name=\"colP8\" columntype=\"thousands\" horizontalalign=\"far\" text=\"持仓盈亏\" width=\"150\" />\r\n                        <th name=\"colP9\" columntype=\"thousands\" horizontalalign=\"far\" text=\"占用保证金\" width=\"100\" />\r\n                        <th name=\"colP10\" columntype=\"text\" horizontalalign=\"center\" text=\"投保\" width=\"60\" />\r\n                        <th name=\"col111\" columntype=\"text\" text=\"交易所\" width=\"80\" />\r\n                        <th name=\"colP12\" columntype=\"int\" horizontalalign=\"far\" text=\"总多仓\" width=\"60\" />\r\n                        <th name=\"colP13\" columntype=\"int\" horizontalalign=\"far\" text=\"总空仓\" width=\"60\" />\r\n                        <th name=\"colP14\" columntype=\"int\" horizontalalign=\"far\" text=\"今多仓\" width=\"60\" />\r\n                        <th name=\"colP15\" columntype=\"int\" horizontalalign=\"far\" text=\"今空仓\" width=\"60\" />\r\n                        <th name=\"colP16\" columntype=\"int\" horizontalalign=\"far\" text=\"总可平今量\" width=\"100\" />\r\n                        <th name=\"colP17\" columntype=\"int\" horizontalalign=\"far\" text=\"总可平仓量\" width=\"100\" />\r\n                        <th name=\"colP18\" columntype=\"int\" horizontalalign=\"far\" text=\"平今挂单量\" width=\"100\" />\r\n                        <th name=\"colP19\" columntype=\"int\" horizontalalign=\"far\" text=\"平仓挂单量\" width=\"100\" />\r\n                        <th name=\"colP20\" columntype=\"int\" horizontalalign=\"far\" text=\"组合冻结量\" width=\"100\" />\r\n                        <th name=\"colP21\" columntype=\"int\" horizontalalign=\"far\" text=\"可平今量\" width=\"80\" />\r\n                        <th name=\"col122\" columntype=\"int\" horizontalalign=\"far\" text=\"可平仓量\" width=\"80\" />\r\n                        <th name=\"colP23\" columntype=\"double\" horizontalalign=\"far\" text=\"开仓均价\" width=\"100\" />\r\n                        <th name=\"colP24\" columntype=\"double\" horizontalalign=\"far\" text=\"多头开仓价\" width=\"100\" />\r\n                        <th name=\"colP25\" columntype=\"double\" horizontalalign=\"far\" text=\"空头开仓价\" width=\"100\" />\r\n                        <th name=\"colP26\" columntype=\"thousands\" horizontalalign=\"far\" text=\"浮动盈亏\" width=\"100\" />\r\n                        <th name=\"colP27\" columntype=\"thousands\" horizontalalign=\"far\" text=\"总盈亏\" width=\"80\" />\r\n                        <th name=\"colP28\" columntype=\"int\" horizontalalign=\"far\" text=\"今开仓量\" width=\"80\" />\r\n                        <th name=\"colP29\" columntype=\"int\" horizontalalign=\"far\" text=\"今平仓量\" width=\"80\" />\r\n                        <th name=\"colP30\" columntype=\"double\" horizontalalign=\"far\" text=\"现价\" width=\"80\" />\r\n                        <th name=\"colP31\" columntype=\"double\" horizontalalign=\"far\" text=\"最新差价\" width=\"80\" />\r\n                      </tr>\r\n                    </table>\r\n                    <table name=\"gridInvestorPositionDetail\" dock=\"fill\" visible=\"false\" bordercolor=\"none\" backcolor=\"none\">\r\n                      <tr>\r\n                        <th name=\"colT1\" columntype=\"text\" text=\"成交编号\" width=\"80\" />\r\n                        <th name=\"colT2\" columntype=\"text\" text=\"合约\" width=\"80\" />\r\n                        <th name=\"colT3\" columntype=\"text\" horizontalalign=\"center\" text=\"多空\" width=\"60\" />\r\n                        <th name=\"colT4\" columntype=\"int\" horizontalalign=\"far\" text=\"手数\" width=\"60\" />\r\n                        <th name=\"colT5\" columntype=\"double\" horizontalalign=\"far\" text=\"开仓价\" width=\"80\" />\r\n                        <th name=\"colT6\" columntype=\"thousands\" horizontalalign=\"far\" text=\"占用保证金\" width=\"100\" />\r\n                        <th name=\"colT7\" columntype=\"text\" text=\"持仓类型\" width=\"80\" />\r\n                        <th name=\"colT8\" columntype=\"text\" horizontalalign=\"center\" text=\"投保\" width=\"60\" />\r\n                        <th name=\"colT9\" columntype=\"text\" horizontalalign=\"center\" text=\"开仓时间\" width=\"100\" />\r\n                        <th name=\"colT10\" columntype=\"thousands\" horizontalalign=\"far\" text=\"持仓盈亏\" width=\"100\" />\r\n                        <th name=\"colT11\" columntype=\"thousands\" horizontalalign=\"far\" text=\"平仓盈亏\" width=\"100\" />\r\n                        <th name=\"colT12\" columntype=\"text\" text=\"交易所\" width=\"80\" />\r\n                        <th name=\"colT13\" columntype=\"text\" text=\"组合状态\" width=\"100\" />\r\n                        <th name=\"colT14\" columntype=\"double\" horizontalalign=\"far\" text=\"昨结算\" width=\"80\" />\r\n                        <th name=\"colT15\" columntype=\"int\" horizontalalign=\"far\" text=\"平仓量\" width=\"80\" />\r\n                        <th name=\"colT16\" columntype=\"thousands\" horizontalalign=\"far\" text=\"浮动盈亏\" width=\"100\" />\r\n                        <th name=\"colT17\" columntype=\"double\" horizontalalign=\"far\" text=\"最新价\" width=\"80\" />\r\n                        <th name=\"colT18\" columntype=\"int\" horizontalalign=\"far\" text=\"组合合约代码\" width=\"100\" />\r\n                      </tr>\r\n                    </table>\r\n                    <table name=\"gridInvestorCombinePositionDetail\" dock=\"fill\" visible=\"false\" bordercolor=\"none\" backcolor=\"none\">\r\n                      <tr>\r\n                        <th name=\"colM1\" columntype=\"text\" text=\"合约\" width=\"120\" />\r\n                        <th name=\"colM2\" columntype=\"text\" horizontalalign=\"center\" text=\"买卖\" width=\"60\" />\r\n                        <th name=\"colM3\" columntype=\"int\" horizontalalign=\"far\" text=\"手数\" width=\"60\" />\r\n                        <th name=\"colM4\" columntype=\"double\" horizontalalign=\"far\" text=\"开仓均价\" width=\"100\" />\r\n                        <th name=\"colM5\" columntype=\"text\" horizontalalign=\"center\" text=\"投保\" width=\"60\" />\r\n                      </tr>\r\n                    </table>\r\n                  </div>\r\n                </div>\r\n              </div>\r\n            </div>\r\n          </div>\r\n        </div>\r\n      </div>\r\n    </div>\r\n  </body>\r\n</html>"

#数值转字符串，可以设置保留位数
#value 数值
#digit 小数位数
def toFixed2(value, digit):
	return str(round(float(value), digit))

#资金账户回调
def onAccountDataCallBack(data, ctpID):
	global m_paint
	gridTradeAccount = findViewByName("gridTradeAccount", m_paint.m_views)
	gridTradeAccount.m_headerHeight = 30
	gridTradeAccount.m_showHScrollBar = TRUE
	for i in range(0,len(gridTradeAccount.m_columns)):
		gridTradeAccount.m_columns[i].m_allowSort = FALSE
		gridTradeAccount.m_columns[i].m_width = 140
	if(len(gridTradeAccount.m_rows) == 0):
		row = FCGridRow()
		gridTradeAccount.m_rows.append(row)
		for i in range(0,len(gridTradeAccount.m_columns)):
			cell1 = FCGridCell()
			row.m_cells.append(cell1)
	gridTradeAccount.m_rows[0].m_cells[0].m_value = toFixed2(data.balance, 0)
	gridTradeAccount.m_rows[0].m_cells[1].m_value = toFixed2(data.closeProfit, 0)
	setCellStyle2(gridTradeAccount.m_rows[0].m_cells[1], data.closeProfit, 0)
	gridTradeAccount.m_rows[0].m_cells[2].m_value = toFixed2(data.floatProfit, 0)
	setCellStyle2(gridTradeAccount.m_rows[0].m_cells[2], data.floatProfit, 0)
	gridTradeAccount.m_rows[0].m_cells[3].m_value = toFixed2(data.positionProfit, 0)
	setCellStyle2(gridTradeAccount.m_rows[0].m_cells[3], data.positionProfit, 0)
	gridTradeAccount.m_rows[0].m_cells[4].m_value = toFixed2(data.dynamicBalance, 0)
	gridTradeAccount.m_rows[0].m_cells[5].m_value = toFixed2(data.currMargin, 0)
	gridTradeAccount.m_rows[0].m_cells[6].m_value = toFixed2(data.frozenCash, 0)
	gridTradeAccount.m_rows[0].m_cells[7].m_value = toFixed2(data.available, 0)
	gridTradeAccount.m_rows[0].m_cells[8].m_value = toFixed2(data.risk * 100, 2) + "%"
	gridTradeAccount.m_rows[0].m_cells[9].m_value = toFixed2(data.frozenMargin, 0)
	gridTradeAccount.m_rows[0].m_cells[10].m_value = toFixed2(data.frozenCommission, 0)
	gridTradeAccount.m_rows[0].m_cells[11].m_value = toFixed2(data.commission, 0)
	gridTradeAccount.m_rows[0].m_cells[12].m_value = toFixed2(data.preBalance, 0)
	gridTradeAccount.m_rows[0].m_cells[13].m_value = toFixed2(data.preCredit, 0)
	gridTradeAccount.m_rows[0].m_cells[14].m_value = toFixed2(data.preMortgage, 0)
	gridTradeAccount.m_rows[0].m_cells[15].m_value = toFixed2(data.mortgage, 0)
	gridTradeAccount.m_rows[0].m_cells[16].m_value = toFixed2(data.withdraw, 0)
	gridTradeAccount.m_rows[0].m_cells[17].m_value = toFixed2(data.deposit, 0)
	gridTradeAccount.m_rows[0].m_cells[18].m_value = toFixed2(data.credit, 0)
	gridTradeAccount.m_rows[0].m_cells[19].m_value = toFixed2(data.reserveBalance, 0)
	gridTradeAccount.m_rows[0].m_cells[20].m_value = toFixed2(data.withdrawQuota, 0)
	invalidateView(gridTradeAccount, gridTradeAccount.m_paint)

#持仓回调
def onInvestorPositionCallBack(data, ctpID):
	global m_paint
	gridInvestorPosition = findViewByName("gridInvestorPosition", m_paint.m_views)
	for i in range(0, len(data)):
		row = None
		for j in range(0, len(gridInvestorPosition.m_rows)):
			if(gridInvestorPosition.m_rows[j].m_cells[0].m_value + gridInvestorPosition.m_rows[j].m_cells[1].m_value == data[i].code + data[i].posiDirection):
				row = gridInvestorPosition.m_rows[j]
				break
		if(row == None):
			row = FCGridRow()
			gridInvestorPosition.m_rows.append(row)
			for j in range(0,len(gridInvestorPosition.m_columns)):
				cell1 = FCGridCell()
				row.m_cells.append(cell1)

		row.m_cells[0].m_value = data[i].code
		row.m_cells[1].m_value = data[i].posiDirection
		row.m_cells[2].m_value = data[i].ydPosition + data[i].todayPosition
		row.m_cells[3].m_value = data[i].ydPosition
		row.m_cells[4].m_value = data[i].todayPosition
		row.m_cells[5].m_value = data[i].position - pyctp.getFrozenAmount(data[i])
		row.m_cells[6].m_value = toFixed2(data[i].positionCost, 0)
		row.m_cells[7].m_value = toFixed2(data[i].positionProfit, 0)
		setCellStyle2(row.m_cells[7], data[i].positionProfit, 0)
		row.m_cells[8].m_value = toFixed2(data[i].margin, 0)
		row.m_cells[9].m_value = data[i].hedgeFlag
		if(data[i].code in m_allCodes):
			row.m_cells[10].m_value = m_allCodes[data[i].code].exchangeID
		else:
			row.m_cells[10].m_value = ""
		row.m_cells[11].m_value = 0
		row.m_cells[12].m_value = 0
		row.m_cells[13].m_value = 0
		row.m_cells[14].m_value = 0
		row.m_cells[15].m_value = 0
		row.m_cells[16].m_value = 0
		row.m_cells[17].m_value = 0
		row.m_cells[18].m_value = 0
		row.m_cells[19].m_value = 0
		row.m_cells[20].m_value = 0
		row.m_cells[21].m_value = 0
		row.m_cells[22].m_value = 0
		row.m_cells[23].m_value = 0
		row.m_cells[24].m_value = 0
		row.m_cells[25].m_value = toFixed2(data[i].floatProfit, 0)
		setCellStyle2(row.m_cells[25], data[i].floatProfit, 0)
		row.m_cells[26].m_value = 0
		row.m_cells[27].m_value = 0
		row.m_cells[28].m_value = 0
		row.m_cells[29].m_value = 0
		row.m_cells[30].m_value = 0
	while(1==1):
		hasValue = FALSE
		rowsSize = len(gridInvestorPosition.m_rows)
		for i in range(0, rowsSize):
			if(gridInvestorPosition.m_rows[i].m_cells[2].m_value == 0):
				gridInvestorPosition.m_rows.pop(i)
				hasValue = TRUE
				break
		if(hasValue == FALSE):
			break
	invalidateView(gridInvestorPosition, gridInvestorPosition.m_paint)

#持仓明细回调
def onInvestorPositionDetailCallBack(data, ctpID):
	global m_paint
	gridInvestorPositionDetail = findViewByName("gridInvestorPositionDetail", m_paint.m_views)
	for i in range(0, len(data)):
		row = None
		for j in range(0, len(gridInvestorPositionDetail.m_rows)):
			if(gridInvestorPositionDetail.m_rows[j].m_cells[0].m_value == data[i].tradeID):
				row = gridInvestorPositionDetail.m_rows[j]
				break
		if(row == None):  
			row = FCGridRow()
			gridInvestorPositionDetail.m_rows.append(row)
			for j in range(0,len(gridInvestorPositionDetail.m_columns)):
				cell1 = FCGridCell()
				row.m_cells.append(cell1)

		row.m_cells[0].m_value = data[i].tradeID
		row.m_cells[1].m_value = data[i].code
		row.m_cells[2].m_value = data[i].direction
		row.m_cells[3].m_value = data[i].volume
		row.m_cells[4].m_value = toFixed2(data[i].openPrice, 0)
		row.m_cells[5].m_value = toFixed2(data[i].margin, 0)
		row.m_cells[6].m_value = data[i].tradeType
		row.m_cells[7].m_value = data[i].hedgeFlag
		row.m_cells[8].m_value = data[i].openDate
		row.m_cells[9].m_value = toFixed2(data[i].positionProfit, 0)
		row.m_cells[10].m_value = toFixed2(data[i].closeProfitByTrade, 0)
		row.m_cells[11].m_value =  data[i].exchangeID
		row.m_cells[12].m_value = "普通持仓"
		row.m_cells[13].m_value = toFixed2(data[i].preSettlementPrice, 0)
		row.m_cells[14].m_value = toFixed2(data[i].closeVolume, 0)
		row.m_cells[15].m_value = toFixed2(data[i].floatProfit, 0)
		row.m_cells[16].m_value = toFixed2(data[i].openPrice, 0)
		row.m_cells[17].m_value = data[i].combInstrumentID
	while(1==1):
		hasValue = FALSE
		rowsSize = len(gridInvestorPositionDetail.m_rows)
		for i in range(0, rowsSize):
			if(gridInvestorPositionDetail.m_rows[i].m_cells[3].m_value == 0):
				gridInvestorPositionDetail.m_rows.pop(i)
				hasValue = TRUE
				break
		if(hasValue == FALSE):
			break
	invalidateView(gridInvestorPositionDetail, gridInvestorPositionDetail.m_paint)

#委托回报回调
def onOrderInfoCallBack(data, ctpID):
	if (data.orderStatus == "未知"):
		return
	if(len(data.orderSysID) == 0):
		return
	global m_paint
	gridOrder = findViewByName("gridOrder", m_paint.m_views)
	row = None
	for j in range(0, len(gridOrder.m_rows)):
		if(gridOrder.m_rows[j].m_cells[0].m_value == data.orderSysID):
			row = gridOrder.m_rows[j]
			break
	if(row == None):
		row = FCGridRow()
		gridOrder.m_rows.insert(0, row)
		for j in range(0,len(gridOrder.m_columns)):
			cell1 = FCGridCell()
			row.m_cells.append(cell1)
	row.m_cells[0].m_value = data.orderSysID
	row.m_cells[1].m_value = data.code
	row.m_cells[2].m_value = data.direction
	row.m_cells[3].m_value = data.combOffsetFlag
	row.m_cells[4].m_value = data.orderStatus
	row.m_cells[5].m_value = toFixed2(data.limitPrice, 0)
	row.m_cells[6].m_value = data.volumeTotalOriginal
	row.m_cells[7].m_value = data.volumeTotal
	row.m_cells[8].m_value = data.volumeTotal
	row.m_cells[9].m_value = data.volumeTraded
	row.m_cells[10].m_value = data.insertTime
	row.m_cells[11].m_value = data.updateTime
	row.m_cells[12].m_value = toFixed2(data.limitPrice, 0)
	row.m_cells[13].m_value = "0"
	row.m_cells[14].m_value = "0"
	row.m_cells[15].m_value = data.combHedgeFlag
	row.m_cells[16].m_value = data.exchangeID
	row.m_cells[17].m_value = data.orderPriceType
	row.m_cells[18].m_value = data.timeCondition
	row.m_cells[19].m_value = data.orderType
	row.m_cells[20].m_value = data.userForceClose
	row.m_cells[21].m_value = data.forceCloseReason
	row.m_cells[22].m_value = ""
	row.m_cells[23].m_value = ""
	invalidateView(gridOrder, gridOrder.m_paint)

#委托回报历史回调
def onOrderInfosCallBack(data, ctpID):
	global m_paint
	gridOrder = findViewByName("gridOrder", m_paint.m_views)
	gridOrder.m_rows = []
	for i in range(0, len(data)):
		if (data[i].orderStatus == "未知"):
			continue
		if(len(data[i].orderSysID) == 0):
			return
		row = None
		for j in range(0, len(gridOrder.m_rows)):
			if(gridOrder.m_rows[j].m_cells[0].m_value == data[i].orderSysID):
				row = gridOrder.m_rows[j]
				break
		if(row == None):
			row = FCGridRow()
			gridOrder.m_rows.insert(0, row)
			for j in range(0,len(gridOrder.m_columns)):
				cell1 = FCGridCell()
				row.m_cells.append(cell1)
		row.m_cells[0].m_value = data[i].orderSysID
		row.m_cells[1].m_value = data[i].code
		row.m_cells[2].m_value = data[i].direction
		row.m_cells[3].m_value = data[i].combOffsetFlag
		row.m_cells[4].m_value = data[i].orderStatus
		row.m_cells[5].m_value = toFixed2(data[i].limitPrice, 0)
		row.m_cells[6].m_value = data[i].volumeTotalOriginal
		row.m_cells[7].m_value = data[i].volumeTotal
		row.m_cells[8].m_value = data[i].volumeTotal
		row.m_cells[9].m_value = data[i].volumeTraded
		row.m_cells[10].m_value = data[i].insertTime
		row.m_cells[11].m_value = data[i].updateTime
		row.m_cells[12].m_value = toFixed2(data[i].limitPrice, 0)
		row.m_cells[13].m_value = "0"
		row.m_cells[14].m_value = "0"
		row.m_cells[15].m_value = data[i].combHedgeFlag
		row.m_cells[16].m_value = data[i].exchangeID
		row.m_cells[17].m_value = data[i].orderPriceType
		row.m_cells[18].m_value = data[i].timeCondition
		row.m_cells[19].m_value = data[i].orderType
		row.m_cells[20].m_value = data[i].userForceClose
		row.m_cells[21].m_value = data[i].forceCloseReason
		row.m_cells[22].m_value = ""
		row.m_cells[23].m_value = ""
	invalidateView(gridOrder, gridOrder.m_paint)


m_allCodes = dict()
m_allDatas = dict()
#码表回调
def onSecurityCallBack(data, ctpID):
	global m_paint
	contractGrid = findViewByName("gridContracts", m_paint.m_views)
	contractGrid.m_rows = []
	for i in range(0, len(data)):
		m_allCodes[data[i].instrumentID] = data[i]
		row = FCGridRow()
		contractGrid.m_rows.append(row)
		cell1 = FCGridCell()
		cell1.m_value = data[i].productID
		row.m_cells.append(cell1)
		cell2 = FCGridCell()
		cell2.m_value = data[i].instrumentID
		row.m_cells.append(cell2)
		cell3 = FCGridCell()
		cell3.m_value = data[i].instrumentName
		row.m_cells.append(cell3)
		cell4 = FCGridCell()
		cell4.m_value = data[i].exchangeID
		row.m_cells.append(cell4)
		cell5 = FCGridCell()
		cell5.m_value = data[i].volumeMultiple
		row.m_cells.append(cell5)
		cell6 = FCGridCell()
		cell6.m_value = data[i].priceTick
		row.m_cells.append(cell6)
		cell7 = FCGridCell()
		cell7.m_value = "期货"
		row.m_cells.append(cell7)
		cell8 = FCGridCell()
		cell8.m_value = data[i].expireDate
		row.m_cells.append(cell8)
		cell9 = FCGridCell()
		cell9.m_value = data[i].longMarginRatio
		row.m_cells.append(cell9)
		cell10 = FCGridCell()
		cell10.m_value = data[i].shortMarginRatio
		row.m_cells.append(cell10)
		cell11 = FCGridCell()
		cell11.m_value = 0
		row.m_cells.append(cell11)
		cell12 = FCGridCell()
		cell12.m_value = 0
		row.m_cells.append(cell12)
		cell13 = FCGridCell()
		cell13.m_value = 0
		row.m_cells.append(cell13)
		cell14 = FCGridCell()
		cell14.m_value = 0
		row.m_cells.append(cell14)
		cell15 = FCGridCell()
		cell15.m_value = 0
		row.m_cells.append(cell15)
		cell16 = FCGridCell()
		cell16.m_value = 0
		row.m_cells.append(cell16)
		cell17 = FCGridCell()
		cell17.m_value = data[i].maxMarketOrderVolume
		row.m_cells.append(cell17)
		cell18 = FCGridCell()
		cell18.m_value = data[i].maxLimitOrderVolume
		row.m_cells.append(cell18)
	invalidateView(contractGrid, contractGrid.m_paint)

#设置单元格的样式
def setCellStyle2(cell, value1, value2):
	if(value1 == None or value2 == None):
		return
	if(float(value1) > float(value2)):
		cell.m_textColor = "rgb(255,0,0)"
	elif(float(value1) < float(value2)):
		cell.m_textColor = "rgb(0,255,0)"
	else:
		cell.m_textColor = "rgb(255,255,255)"

#当前的代码
m_currentCode = ""

#最新数据回调
def onSecurityLatestDataCallBack(data, ctpID):
	global m_paint	
	gridLatestData = findViewByName("gridLatestData", m_paint.m_views)
	chart = findViewByName("chart", m_paint.m_views)
	for d in range(0, len(data)):
		row = None
		for i in range(0, len(gridLatestData.m_rows)):
			if(gridLatestData.m_rows[i].m_cells[0].m_value == data[d].code):
				row = gridLatestData.m_rows[i]
				break
		if(row == None):
			row = FCGridRow()
			gridLatestData.m_rows.append(row)
			for j in range(0,len(gridLatestData.m_columns)):
				cell1 = FCGridCell()
				row.m_cells.append(cell1)
		row.m_cells[0].m_value = data[d].code
		newVol = 0
		if(data[d].code in m_allDatas):
			newVol = data[d].volume - m_allDatas[data[d].code].volume
		m_allDatas[data[d].code] = data[d]
		digit = 0
		if(data[d].code in m_allCodes):
			row.m_cells[1].m_value = m_allCodes[data[d].code].instrumentName
			digit = m_allCodes[data[d].code].digit
		setCellStyle2(row.m_cells[2], row.m_cells[2].m_value, data[d].close)
		row.m_cells[2].m_value = toFixed2(data[d].close, digit)
		diff = data[d].close - data[d].preSettlementPrice
		setCellStyle2(row.m_cells[3], diff, 0)
		row.m_cells[3].m_value = toFixed2(diff, digit)
		setCellStyle2(row.m_cells[4], row.m_cells[4].m_value, data[d].bidPrice1)
		row.m_cells[4].m_value = toFixed2(data[d].bidPrice1, digit)
		row.m_cells[5].m_value = data[d].bidVolume1
		setCellStyle2(row.m_cells[6], row.m_cells[6].m_value, data[d].askPrice1)
		row.m_cells[6].m_value = toFixed2(data[d].askPrice1, digit)
		row.m_cells[7].m_value = data[d].askVolume1
		row.m_cells[8].m_value = data[d].volume
		row.m_cells[9].m_value = toFixed2(data[d].openInterest, digit)
		row.m_cells[10].m_value = toFixed2(data[d].upperLimit, digit)
		row.m_cells[11].m_value = toFixed2(data[d].lowerLimit, digit)
		setCellStyle2(row.m_cells[12], row.m_cells[12].m_value, data[d].open)
		row.m_cells[12].m_value = toFixed2(data[d].open, digit)
		row.m_cells[13].m_value = toFixed2(data[d].preSettlementPrice, digit)
		setCellStyle2(row.m_cells[14], row.m_cells[14].m_value, data[d].high)
		row.m_cells[14].m_value = toFixed2(data[d].high, digit)
		setCellStyle2(row.m_cells[15], row.m_cells[15].m_value, data[d].low)
		row.m_cells[15].m_value = toFixed2(data[d].low, digit)
		row.m_cells[16].m_value = data[d].bidVolume1
		rangeValue = 0
		if(data[d].preSettlementPrice != 0):
			rangeValue = 100 * (data[d].close - data[d].preSettlementPrice) / data[d].preSettlementPrice
		row.m_cells[17].m_value = toFixed2(rangeValue, digit) + "%"
		setCellStyle2(row.m_cells[17], rangeValue, 0)
		row.m_cells[18].m_value = toFixed2(data[d].preClose, digit)
		row.m_cells[19].m_value = data[d].turnover
		row.m_cells[20].m_value = data[d].exchangeID
		row.m_cells[21].m_value = data[d].updateTime
		row.m_cells[22].m_value = toFixed2(data[d].preOpenInterest, digit)
		row.m_cells[23].m_value = toFixed2(data[d].close, digit)
		row.m_cells[24].m_value = toFixed2(data[d].settlementPrice, digit)
		row.m_cells[25].m_value = toFixed2(data[d].averagePrice, digit)
		row.m_cells[26].m_value = 0
		row.m_cells[27].m_value = 0
		row.m_cells[28].m_value = 0
		row.m_cells[29].m_value = 0
		row.m_cells[30].m_value = 0
		row.m_cells[31].m_value = 0
		if(newVol > 0):
			if(data[d].code == m_currentCode):
				sData = SecurityData()
				sData.m_date = len(chart.m_data) + 1
				sData.m_close = data[d].close
				sData.m_open = data[d].close
				sData.m_high = data[d].close
				sData.m_low = data[d].close
				sData.m_volume = newVol
				chart.m_data.append(sData)
				calculateChartMaxMin(chart)
				invalidateView(chart, chart.m_paint)
	invalidateView(gridLatestData, gridLatestData.m_paint)

#成交回报回调
def onTradeRecordCallBack(data, ctpID):
	if(len(data.tradeID) == 0):
		return
	global m_paint
	gridTradeRecord = findViewByName("gridTradeRecord", m_paint.m_views)
	row = FCGridRow()
	gridTradeRecord.m_rows.insert(0, row)
	cell1 = FCGridCell()
	cell1.m_value = data.tradeID
	row.m_cells.append(cell1)
	cell2 = FCGridCell()
	cell2.m_value = data.code
	row.m_cells.append(cell2)
	cell3 = FCGridCell()
	cell3.m_value = data.direction
	row.m_cells.append(cell3)
	cell4 = FCGridCell()
	cell4.m_value = data.offsetFlag
	row.m_cells.append(cell4)
	cell5 = FCGridCell()
	cell5.m_value = toFixed2(data.price, 0)
	row.m_cells.append(cell5)
	cell6 = FCGridCell()
	cell6.m_value = toFixed2(data.volume, 0)
	row.m_cells.append(cell6)
	cell7 = FCGridCell()
	cell7.m_value = data.tradeTime
	row.m_cells.append(cell7)
	cell8 = FCGridCell()
	cell8.m_value = data.orderSysID
	row.m_cells.append(cell8)
	cell9 = FCGridCell()
	cell9.m_value = "普通成交"
	row.m_cells.append(cell9)
	cell10 = FCGridCell()
	cell10.m_value = data.hedgeFlag
	row.m_cells.append(cell10)
	cell11 = FCGridCell()
	cell11.m_value = data.exchangeID
	row.m_cells.append(cell11)
	cell12 = FCGridCell()
	cell12.m_value = data.commission
	row.m_cells.append(cell12)
	invalidateView(gridTradeRecord, gridTradeRecord.m_paint)

#成交回报历史回调
def onTradeRecordsCallBack(data, ctpID):
	global m_paint
	gridTradeRecord = findViewByName("gridTradeRecord", m_paint.m_views)
	gridTradeRecord.m_rows = []
	for i in range(0, len(data)):
		if(len(data[i].tradeID) == 0):
			return
		row = FCGridRow()
		gridTradeRecord.m_rows.insert(0, row)
		cell1 = FCGridCell()
		cell1.m_value = data[i].tradeID
		row.m_cells.append(cell1)
		cell2 = FCGridCell()
		cell2.m_value = data[i].code
		row.m_cells.append(cell2)
		cell3 = FCGridCell()
		cell3.m_value = data[i].direction
		row.m_cells.append(cell3)
		cell4 = FCGridCell()
		cell4.m_value = data[i].offsetFlag
		row.m_cells.append(cell4)
		cell5 = FCGridCell()
		cell5.m_value = toFixed2(data[i].price, 0)
		row.m_cells.append(cell5)
		cell6 = FCGridCell()
		cell6.m_value = toFixed2(data[i].volume, 0)
		row.m_cells.append(cell6)
		cell7 = FCGridCell()
		cell7.m_value = data[i].tradeTime
		row.m_cells.append(cell7)
		cell8 = FCGridCell()
		cell8.m_value = data[i].orderSysID
		row.m_cells.append(cell8)
		cell9 = FCGridCell()
		cell9.m_value = "普通成交"
		row.m_cells.append(cell9)
		cell10 = FCGridCell()
		cell10.m_value = data[i].hedgeFlag
		row.m_cells.append(cell10)
		cell11 = FCGridCell()
		cell11.m_value = data[i].exchangeID
		row.m_cells.append(cell11)
		cell12 = FCGridCell()
		cell12.m_value = data[i].commission
		row.m_cells.append(cell12)
	invalidateView(gridTradeRecord, gridTradeRecord.m_paint)

ctp = None #ctp

#检查CTP的数据
def checkCTPData(a='', b=''):
	global ctp
	while (ctp.hasNewDatas()):
		recvData = create_string_buffer(102400)
		if (ctp.getDepthMarketData(recvData) > 0):
			data = pyctp.convertToCTPDepthMarketData(str(recvData.value, encoding="gbk"))
			onSecurityLatestDataCallBack(data, ctp.m_ctpID)
			continue
		if (ctp.getAccountData(recvData) > 0):
			data = pyctp.convertToCTPAccountData(str(recvData.value, encoding="gbk"))
			onAccountDataCallBack(data, ctp.m_ctpID)
			continue
		if (ctp.getOrderInfo(recvData) > 0):
			data = pyctp.convertToCTPOrder(str(recvData.value, encoding="gbk"))
			onOrderInfoCallBack(data, ctp.m_ctpID)
			continue
		if (ctp.getTradeRecord(recvData) > 0):
			data = pyctp.convertToCTPTrade(str(recvData.value, encoding="gbk"))
			onTradeRecordCallBack(data, ctp.m_ctpID)
			continue
		if (ctp.getPositionData(recvData) > 0):
			data = pyctp.convertToCTPInvestorPosition(str(recvData.value, encoding="gbk"))
			onInvestorPositionCallBack(data, ctp.m_ctpID)
			continue
		if (ctp.getPositionDetailData(recvData) > 0):
			data = pyctp.convertToCTPInvestorPositionDetail(str(recvData.value, encoding="gbk"))
			onInvestorPositionDetailCallBack(data, ctp.m_ctpID)
			continue
		break

#启动CTP
def runCTP():
	global ctp
	ctp = pyctp.CTPDLL()
	ctp.init()
	ctp.m_ctpID = ctp.create()
	reqID = ctp.generateReqID()
	# 启动CTP交易和行情
	ctp.start(reqID, "simnow_client_test", "0000000000000000", "180.168.146.187:10212", "180.168.146.187:10202", "9999", "021739", "123456")
	# 检查是否登陆成功
	while (ctp.isDataOk() <= 0):
		time.sleep(1)
	print("登陆CTP成功!")
	recvData = create_string_buffer(1024 * 1024 * 10)
	if (ctp.getInstrumentsData(recvData) > 0):
		data = pyctp.convertToCTPInstrumentDatas(str(recvData.value, encoding="gbk"))
		onSecurityCallBack(data, ctp.m_ctpID)
	recvData = create_string_buffer(1024 * 1024 * 10)
	if (ctp.getOrderInfos(recvData) > 0):
		data = pyctp.convertToCTPOrderList(str(recvData.value, encoding="gbk"))
		onOrderInfosCallBack(data, ctp.m_ctpID)
	recvData = create_string_buffer(1024 * 1024 * 10)
	if (ctp.getTradeRecords(recvData) > 0):
		data = pyctp.convertToCTPTradeRecords(str(recvData.value, encoding="gbk"))
		onTradeRecordsCallBack(data, ctp.m_ctpID)
	# 注册行情
	reqID = ctp.generateReqID()
	ctp.subMarketDatas(reqID, "cu2301,cu2302,cu2303,rb2301,rb2302,rb2304,ru2301,ru2302,ru2303")
	timer.set_timer(1, checkCTPData)

#点击单元格
def onClickGridCell(grid, row, gridColumn, cell, firstTouch, secondTouch, firstPoint, secondPoint):
	global m_paint
	global m_currentCode
	gridName = grid.m_name
	if (gridName == "gridLatestData"):
		chart = findViewByName("chart", m_paint.m_views)
		chart.m_data = []
		calculateChartMaxMin(chart)
		code = row.m_cells[0].m_value
		m_currentCode = code
		price = row.m_cells[2].m_value
		txtIssueCode = findViewByName("txtIssueCode", m_paint.m_views)
		spinPrice = findViewByName("spinPrice", m_paint.m_views)
		spinVolume = findViewByName("spinVolume", m_paint.m_views)
		setViewAttribute(txtIssueCode, "text", code)
		setViewAttribute(spinPrice, "text", price)
		setViewAttribute(spinVolume, "text", "1")
		invalidate(m_paint)
	elif(gridName == "gridInvestorPosition"):
		code = row.m_cells[0].m_value
		price = ""
		if(code in m_allDatas):
			price = str(m_allDatas[code].close)
		txtIssueCode = findViewByName("txtIssueCode", m_paint.m_views)
		spinPrice = findViewByName("spinPrice", m_paint.m_views)
		spinVolume = findViewByName("spinVolume", m_paint.m_views)
		setViewAttribute(txtIssueCode, "text", code)
		setViewAttribute(spinPrice, "text", price)
		setViewAttribute(spinVolume, "text", "1")
		invalidate(m_paint)
	elif(gridName == "gridInvestorPositionDetail"):
		code = row.m_cells[1].m_value
		price = ""
		if(code in m_allDatas):
			price = str(m_allDatas[code].close)
		txtIssueCode = findViewByName("txtIssueCode", m_paint.m_views)
		spinPrice = findViewByName("spinPrice", m_paint.m_views)
		spinVolume = findViewByName("spinVolume", m_paint.m_views)
		setViewAttribute(txtIssueCode, "text", code)
		setViewAttribute(spinPrice, "text", price)
		setViewAttribute(spinVolume, "text", "1")
		invalidate(m_paint)

m_paint = FCPaint() #创建绘图对象
facecat.m_paintCallBack = onViewPaint 
facecat.m_paintBorderCallBack = onViewPaintBorder 
facecat.m_mouseDownCallBack = onViewMouseDown 
facecat.m_mouseMoveCallBack = onViewMouseMove 
facecat.m_mouseUpCallBack = onViewMouseUp
facecat.m_mouseWheelCallBack = onViewMouseWheel
facecat.m_mouseEnterCallBack = onViewMouseEnter
facecat.m_mouseLeaveCallBack = onViewMouseLeave
facecat.m_clickCallBack = onViewClick
facecat.m_clickGridCellCallBack = onClickGridCell

#消息循环
def WndProc(hwnd,msg,wParam,lParam):
	if msg == WM_DESTROY:
		os._exit(0)
		win32gui.PostQuitMessage(0)
	if(hwnd == m_paint.m_hWnd):
		if msg == WM_ERASEBKGND:
			return 1
		elif msg == WM_SIZE:
			rect = win32gui.GetClientRect(m_paint.m_hWnd)
			m_paint.m_size = FCSize(rect[2] - rect[0], rect[3] - rect[1])
			for view in m_paint.m_views:
				if view.m_dock == "fill":
					view.m_size = FCSize(m_paint.m_size.cx, m_paint.m_size.cy)
			updateView(m_paint.m_views)
			invalidate(m_paint)
		elif msg == WM_LBUTTONDOWN:
			mx, my = win32api.GetCursorPos()
			ccx, ccy = win32gui.ScreenToClient(hwnd, (mx, my))
			mp = FCPoint(ccx, ccy)
			onMouseDown(mp, 1, 1, 0, m_paint)
		elif msg == WM_LBUTTONDBLCLK:
			mx, my = win32api.GetCursorPos()
			ccx, ccy = win32gui.ScreenToClient(hwnd, (mx, my))
			mp = FCPoint(ccx, ccy)
			onMouseDown(mp, 1, 2, 0, m_paint)
		elif msg == WM_LBUTTONUP:
			mx, my = win32api.GetCursorPos()
			ccx, ccy = win32gui.ScreenToClient(hwnd, (mx, my))
			mp = FCPoint(ccx, ccy)
			onMouseUp(mp, 1, 1, 0, m_paint)
		elif msg == WM_MOUSEWHEEL:
			mx, my = win32api.GetCursorPos()
			ccx, ccy = win32gui.ScreenToClient(hwnd, (mx, my))
			mp = FCPoint(ccx, ccy)
			if(wParam > 4000000000):
				onMouseWheel(mp, 0, 0, -1, m_paint)
			else:
				onMouseWheel(mp, 0, 0, 1, m_paint)
		elif msg == WM_MOUSEMOVE:
			mx, my = win32api.GetCursorPos()
			ccx, ccy = win32gui.ScreenToClient(hwnd, (mx, my))
			mp = FCPoint(ccx, ccy)
			if(wParam == 1):
				onMouseMove(mp, 1, 1, 0, m_paint)
			elif(wParam == 2):
				onMouseMove(mp, 2, 1, 0, m_paint)
			else:
				onMouseMove(mp, 0, 0, 0, m_paint)
		elif msg == WM_PAINT:
			rect = win32gui.GetClientRect(m_paint.m_hWnd)
			m_paint.m_size = FCSize(rect[2] - rect[0], rect[3] - rect[1])
			for view in m_paint.m_views:
				if view.m_dock == "fill":
					view.m_size = FCSize(m_paint.m_size.cx, m_paint.m_size.cy)
			updateView(m_paint.m_views)
			invalidate(m_paint)
		elif msg == WM_IME_COMPOSITION or msg == WM_IME_CHAR or msg == WM_IME_SETCONTEXT:
			if(m_paint.m_useGdiPlus):
				m_paint.m_gdiPlusPaint.onMessage(hwnd,msg,wParam,lParam)
		elif msg == WM_CHAR or msg == WM_KEYDOWN or msg == WM_SYSKEYDOWN or msg == WM_KEYUP or msg == WM_SYSKEYUP:
			if(facecat.m_focusedView != None and facecat.m_focusedView.m_exView):
				if(m_paint.m_useGdiPlus):
					m_paint.m_gdiPlusPaint.onMessage(hwnd,msg,wParam,lParam)
					invalidateView(facecat.m_focusedView, facecat.m_focusedView.m_paint)
	return win32gui.DefWindowProc(hwnd,msg,wParam,lParam)
	
#创建窗体
wc = win32gui.WNDCLASS()
wc.hbrBackground = COLOR_BTNFACE + 1
wc.hCursor = win32gui.LoadCursor(0,IDI_APPLICATION)
wc.lpszClassName = "facecat-py"
wc.lpfnWndProc = WndProc
wc.style = CS_HREDRAW | CS_VREDRAW | CS_DBLCLKS
reg = win32gui.RegisterClass(wc)
hwnd = win32gui.CreateWindow(reg,'facecat-py',WS_OVERLAPPEDWINDOW | WS_CLIPCHILDREN,CW_USEDEFAULT,CW_USEDEFAULT,CW_USEDEFAULT,CW_USEDEFAULT,0,0,0,None)
m_paint.m_hWnd = hwnd

#读取XML
root  = ET.fromstring(m_xml)
for child in root:
	if(child.tag == "{facecat}body"):
		readXmlNode(m_paint, child, None)
chart = findViewByName("chart", m_paint.m_views)
chart.m_candleDivPercent = 0.7
chart.m_volDivPercent = 0.3
chart.m_indDivPercent = 0
chart.m_cycle = "trend"
rect = win32gui.GetClientRect(hwnd)
m_paint.m_size = FCSize(rect[2] - rect[0], rect[3] - rect[1])
for view in m_paint.m_views:
	if view.m_dock == "fill":
		view.m_size = FCSize(m_paint.m_size.cx, m_paint.m_size.cy)
updateView(m_paint.m_views)
win32gui.ShowWindow(hwnd,SW_SHOWNORMAL)
win32gui.UpdateWindow(hwnd)
runCTP()
win32gui.PumpMessages()
