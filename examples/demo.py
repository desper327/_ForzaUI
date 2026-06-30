# -*- coding: utf-8 -*-
"""
forza_ui 全组件学习示例
======================

运行方式：
    python examples/demo.py

左侧按 forza_ui 目录分类浏览，右侧为可滚动展示区。
每个区块都有中文注释，说明组件用途、常用写法和链式 API。

学习路径建议：
    1. basic    → 文字、头像、角标等静态展示
    2. input    → 表单输入与按钮操作（最常用）
    3. display  → 表格/树/卡片（需自备 Model）
    4. navigation → 标签页、折叠、菜单、抽屉
    5. feedback → 提示、加载、进度
    6. layout   → 流式布局、分割面板等

MVC 实战见：examples/mvc_panel_example.py
"""

from __future__ import annotations

import _bootstrap  # noqa: F401  自动把 forza_ui 和 Qt.py 加入 sys.path

from Qt import QtCore, QtGui, QtWidgets

from forza_ui import forza_theme
from forza_ui.icons import FIcon, FPixmap
from forza_ui.utils import application


# --- basic 基础展示 ---
from forza_ui.basic.avatar import FAvatar
from forza_ui.basic.badge import FBadge
from forza_ui.basic.divider import FDivider
from forza_ui.basic.label import FLabel

# --- input 输入与操作 ---
from forza_ui.input.button_group import (
    FCheckBoxGroup,
    FPushButtonGroup,
    FRadioButtonGroup,
    FToolButtonGroup,
)
from forza_ui.input.check_box import FCheckBox
from forza_ui.input.combo_box import FComboBox
from forza_ui.input.completer import FCompleter
from forza_ui.input.line_edit import FLineEdit
from forza_ui.input.push_button import FPushButton
from forza_ui.input.radio_button import FRadioButton
from forza_ui.input.slider import FSlider
from forza_ui.input.spin_box import (
    FDateEdit,
    FDateTimeEdit,
    FDoubleSpinBox,
    FSpinBox,
    FTimeEdit,
)
from forza_ui.input.switch import FSwitch
from forza_ui.input.text_edit import FTextEdit
from forza_ui.input.tool_button import FToolButton

# --- display 数据展示 ---
from forza_ui.display.card import FCard, FMeta
from forza_ui.display.carousel import FCarousel
from forza_ui.display.item_view import FBigView, FListView, FTableView, FTreeView

# --- navigation 导航与结构 ---
from forza_ui.navigation.collapse import FCollapse
from forza_ui.navigation.drawer import FDrawer
from forza_ui.navigation.line_tab_widget import FLineTabWidget
from forza_ui.navigation.menu import FMenu
from forza_ui.navigation.menu_tab_widget import FMenuTabWidget
from forza_ui.navigation.tab_widget import FTabWidget

# --- feedback 反馈与状态 ---
from forza_ui.feedback.alert import FAlert
from forza_ui.feedback.loading import FLoading, FLoadingWrapper
from forza_ui.feedback.message import FMessage
from forza_ui.feedback.progress_bar import FProgressBar
from forza_ui.feedback.progress_circle import FProgressCircle
from forza_ui.feedback.toast import FToast

# --- layout 布局与容器 ---
from forza_ui.layout.flow_layout import FFlowLayout
from forza_ui.layout.splitter import FSplitter


# ---------------------------------------------------------------------------
# 页面构建辅助
# ---------------------------------------------------------------------------

def _section(title: str, tip: str) -> QtWidgets.QWidget:
    """每个组件区块的标题 + 说明文字。"""
    box = QtWidgets.QWidget()
    lay = QtWidgets.QVBoxLayout(box)
    lay.setContentsMargins(0, 12, 0, 4)
    lay.addWidget(FLabel(title).h4())
    lay.addWidget(FLabel(tip).secondary())
    lay.addWidget(FDivider())
    return box


def _scroll_page(build_fn) -> QtWidgets.QScrollArea:
    """把页面内容放进 QScrollArea，避免组件过多时窗口撑不下。"""
    inner = QtWidgets.QWidget()
    inner.setLayout(QtWidgets.QVBoxLayout())
    inner.layout().setContentsMargins(16, 8, 16, 16)
    build_fn(inner.layout())
    inner.layout().addStretch()

    scroll = QtWidgets.QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setFrameShape(QtWidgets.QFrame.NoFrame)
    scroll.setWidget(inner)
    return scroll


def _demo_table_model() -> QtGui.QStandardItemModel:
    """forza_ui 视图类不内置 Model，示例里用 QStandardItemModel 演示。"""
    model = QtGui.QStandardItemModel(3, 3)
    model.setHorizontalHeaderLabels(["名称", "类型", "状态"])
    rows = [
        ("Camera_A", "相机", "完成"),
        ("Char_Hero", "角色", "进行中"),
        ("Env_City", "场景", "待开始"),
    ]
    for r, row in enumerate(rows):
        for c, text in enumerate(row):
            model.setItem(r, c, QtGui.QStandardItem(text))
    return model


def _demo_tree_model() -> QtGui.QStandardItemModel:
    model = QtGui.QStandardItemModel()
    root = model.invisibleRootItem()
    shot = QtGui.QStandardItem("Shot_010")
    shot.appendRow(QtGui.QStandardItem("Animation"))
    shot.appendRow(QtGui.QStandardItem("Lighting"))
    asset = QtGui.QStandardItem("Assets")
    asset.appendRow(QtGui.QStandardItem("Model"))
    asset.appendRow(QtGui.QStandardItem("Texture"))
    root.appendRow(shot)
    root.appendRow(asset)
    return model


# ---------------------------------------------------------------------------
# 1. basic — 基础展示
# ---------------------------------------------------------------------------

def _build_basic_page(layout: QtWidgets.QVBoxLayout) -> None:
    # --- FLabel：标题/正文，链式方法设置层级和样式 ---
    layout.addWidget(_section(
        "FLabel",
        "路径：forza_ui/basic/label.py | 替代 QLabel，支持 h1–h4、强调、链接等。",
    ))
    label_row = QtWidgets.QHBoxLayout()
    label_row.addWidget(FLabel("H1 标题").h1())
    label_row.addWidget(FLabel("次要文字").secondary())
    label_row.addWidget(FLabel("警告").warning())
    label_row.addWidget(FLabel("危险").danger())
    label_row.addWidget(FLabel("加粗").strong())
    label_wrap = QtWidgets.QWidget()
    label_wrap.setLayout(label_row)
    layout.addWidget(label_wrap)

    link = FLabel()
    link.set_link("https://github.com/phenom-films/dayu_widgets", text="超链接示例")
    layout.addWidget(link)

    # --- FDivider：带文字的分隔线 ---
    layout.addWidget(_section("FDivider", "路径：forza_ui/basic/divider.py"))
    layout.addWidget(FDivider.center("居中分隔线"))
    layout.addWidget(FDivider.left("左对齐分隔线"))

    # --- FAvatar：圆形头像/图标 ---
    layout.addWidget(_section(
        "FAvatar",
        "路径：forza_ui/basic/avatar.py | set_fui_image() 设置图片，.huge()/.tiny() 设置尺寸。",
    ))
    avatar_row = QtWidgets.QHBoxLayout()
    avatar_row.addWidget(FAvatar.huge())
    avatar_row.addWidget(FAvatar.large())
    avatar_row.addWidget(FAvatar.medium())
    avatar_row.addWidget(FAvatar.small())
    avatar_row.addWidget(FAvatar.tiny())
    avatar_wrap = QtWidgets.QWidget()
    avatar_wrap.setLayout(avatar_row)
    layout.addWidget(avatar_wrap)

    # --- FBadge：角标，包裹在其它控件右上角 ---
    layout.addWidget(_section(
        "FBadge",
        "路径：forza_ui/basic/badge.py | FBadge.dot/count/text 工厂方法创建三种样式。",
    ))
    badge_row = QtWidgets.QHBoxLayout()
    dot_btn = FPushButton("消息").primary()
    badge_row.addWidget(FBadge.dot(show=True, widget=dot_btn))
    count_btn = FPushButton("通知")
    b=FBadge.count(count=8, widget=count_btn)
    badge_row.addWidget(b)
    text_btn = FToolButton().svg("user_line.svg").medium()
    badge_row.addWidget(FBadge.text(text="NEW", widget=text_btn))
    badge_wrap = QtWidgets.QWidget()
    badge_wrap.setLayout(badge_row)
    layout.addWidget(badge_wrap)

    b.set_fui_count(10000)
    b.set_fui_overflow(100)#超过100显示100+


# ---------------------------------------------------------------------------
# 2. input — 输入与操作
# ---------------------------------------------------------------------------

def _build_input_page(layout: QtWidgets.QVBoxLayout) -> None:
    # --- FPushButton：主按钮，链式设置类型和尺寸 ---
    layout.addWidget(_section(
        "FPushButton",
        "路径：forza_ui/input/push_button.py | .primary()/.success()/.warning()/.danger() + .medium()",
    ))
    btn_row = QtWidgets.QHBoxLayout()
    btn_row.addWidget(FPushButton("Default"))
    btn_row.addWidget(FPushButton("Primary").primary())
    btn_row.addWidget(FPushButton("Success").success())
    btn_row.addWidget(FPushButton("Warning").warning())
    btn_row.addWidget(FPushButton("Danger").danger())
    btn_wrap = QtWidgets.QWidget()
    btn_wrap.setLayout(btn_row)
    layout.addWidget(btn_wrap)

    size_row = QtWidgets.QHBoxLayout()
    for name, method in [
        ("huge", "huge"), ("large", "large"), ("medium", "medium"),
        ("small", "small"), ("tiny", "tiny"),
    ]:
        b = FPushButton(name)
        getattr(b, method)()#直接调用方法，而不是通过字符串调用
        size_row.addWidget(b)
    size_wrap = QtWidgets.QWidget()
    size_wrap.setLayout(size_row)
    layout.addWidget(size_wrap)

    # --- FToolButton：图标按钮 ---
    layout.addWidget(_section(
        "FToolButton",
        "路径：forza_ui/input/tool_button.py | .svg('xxx.svg') 加载内置图标，.icon_only()",
    ))
    tool_row = QtWidgets.QHBoxLayout()
    for svg in ("home_line.svg", "search_line.svg", "edit_line.svg", "trash_line.svg"):
        t=FToolButton().svg(svg).medium().text_under_icon()#.text_beside_icon()
        t.setText(svg.split(".")[0].capitalize())#设置文本
        tool_row.addWidget(t)#.icon_only()
    tool_wrap = QtWidgets.QWidget()
    tool_wrap.setLayout(tool_row)
    layout.addWidget(tool_wrap)

    # --- 文本输入 ---
    layout.addWidget(_section("FLineEdit / FTextEdit / FComboBox", "路径：forza_ui/input/"))
    line = FLineEdit().medium()
    line.set_suffix_widget(FToolButton().svg("search_line.svg").medium().text_under_icon())
    line.setPlaceholderText("FLineEdit：单行输入，监听 textChanged 信号")
    layout.addWidget(line)

    text_edit = FTextEdit()
    text_edit.setPlaceholderText("FTextEdit：多行文本")
    text_edit.setMaximumHeight(80)
    layout.addWidget(text_edit)

    combo = FComboBox().medium()
    combo.addItems(["Option A", "Option B", "Option C"])
    layout.addWidget(combo)

    # FCompleter：配合 FLineEdit 做输入补全
    completer_edit = FLineEdit().medium()
    completer_edit.setPlaceholderText("输入 ma/mb/my 试试补全")
    words = ["maya", "max", "houdini", "nuke", "blender"]
    completer = FCompleter(words)
    completer_edit.setCompleter(completer)
    layout.addWidget(completer_edit)

    # --- 选择类控件 ---
    layout.addWidget(_section("FCheckBox / FRadioButton / FSwitch", "路径：forza_ui/input/"))
    check_row = QtWidgets.QHBoxLayout()
    check_row.addWidget(FCheckBox("启用缓存"))
    check_row.addWidget(FRadioButton("选项 A"))
    check_row.addWidget(FRadioButton("选项 B"))
    check_row.addWidget(FSwitch())
    check_wrap = QtWidgets.QWidget()
    check_wrap.setLayout(check_row)
    layout.addWidget(check_wrap)

    # --- 数值 / 日期 ---
    layout.addWidget(_section("FSpinBox / FSlider / 日期时间", "路径：forza_ui/input/spin_box.py"))
    spin_row = QtWidgets.QHBoxLayout()
    spin = FSpinBox()
    spin.setRange(0, 100)
    spin.setValue(42)
    spin_row.addWidget(spin)
    spin_row.addWidget(FDoubleSpinBox())
    spin_row.addWidget(FSlider(QtCore.Qt.Horizontal))
    spin_wrap = QtWidgets.QWidget()
    spin_wrap.setLayout(spin_row)
    layout.addWidget(spin_wrap)

    date_row = QtWidgets.QHBoxLayout()
    date_row.addWidget(FDateEdit())
    date_row.addWidget(FTimeEdit())
    date_row.addWidget(FDateTimeEdit())
    date_wrap = QtWidgets.QWidget()
    date_wrap.setLayout(date_row)
    layout.addWidget(date_wrap)

    # --- 按钮组：批量创建互斥/多选按钮 ---
    layout.addWidget(_section(
        "Button Groups",
        "路径：forza_ui/input/button_group.py | set_button_list([{text:...}, ...]) 批量添加",
    ))
    push_grp = FPushButtonGroup()
    push_grp.set_button_list([{"text": "左"}, {"text": "中"}, {"text": "右"}])
    layout.addWidget(push_grp)

    radio_grp = FRadioButtonGroup()
    radio_grp.set_button_list([{"text": "低"}, {"text": "中"}, {"text": "高"}])
    radio_grp.set_fui_checked(1)
    layout.addWidget(radio_grp)

    check_grp = FCheckBoxGroup()
    check_grp.set_button_list([
        {"text": "灯光", "checkable": True, "checked": True},
        {"text": "动画", "checkable": True},
        {"text": "特效", "checkable": True},
    ])
    layout.addWidget(check_grp)

    tool_grp = FToolButtonGroup(exclusive=True)
    tool_grp.set_button_list([
        {"svg": "list_view.svg"},
        {"svg": "tree_view.svg"},
        {"svg": "table_view.svg"},
    ])
    tool_grp.set_fui_checked(0)
    layout.addWidget(tool_grp)


# ---------------------------------------------------------------------------
# 3. display — 数据展示
# ---------------------------------------------------------------------------

def _build_display_page(layout: QtWidgets.QVBoxLayout) -> None:
    layout.addWidget(_section(
        "Item Views",
        "路径：forza_ui/display/item_view.py | 必须 setModel()，forza_ui 不提供内置 Model。",
    ))

    table = FTableView()
    table.setModel(_demo_table_model())
    table.setMinimumHeight(120)
    layout.addWidget(table)

    tree = FTreeView()
    tree.setModel(_demo_tree_model())
    tree.setMinimumHeight(120)
    layout.addWidget(tree)

    list_view = FListView()
    list_model = QtCore.QStringListModel(["Take_01", "Take_02", "Take_03"]*30)
    list_view.setModel(list_model)
    list_view.setMinimumHeight(80)
    layout.addWidget(list_view)

    big_view = FBigView()
    big_view.setModel(list_model)
    big_view.setMinimumHeight(100)
    layout.addWidget(big_view)

    # --- FCard / FMeta：信息卡片 ---
    layout.addWidget(_section("FCard / FMeta", "路径：forza_ui/display/card.py"))
    card = FCard(title="任务卡片", extra=True)
    meta = FMeta(extra=True)
    meta.setup_data({
        "title": "镜头 Shot_010",
        "description": "动画 blocking 阶段，截止周五。",
        "avatar": FPixmap("user_fill.svg"),
    })
    meta.get_more_button().setVisible(True)
    card.set_widget(meta)
    card.setMaximumWidth(360)
    layout.addWidget(card)

    # --- FCarousel：轮播图，传入 QPixmap 列表 ---
    layout.addWidget(_section(
        "FCarousel",
        "路径：forza_ui/display/carousel.py | FCarousel([pixmap, ...], width=, height=)",
    ))
    pix_list = [
        FPixmap("app-maya.png"),
        FPixmap("app-nuke.png"),
        FPixmap("app-houdini.png"),
    ]
    carousel = FCarousel(pix_list, width=320, height=180, autoplay=True)
    layout.addWidget(carousel)


# ---------------------------------------------------------------------------
# 4. navigation — 导航与结构
# ---------------------------------------------------------------------------

def _build_navigation_page(layout: QtWidgets.QVBoxLayout, host: QtWidgets.QWidget) -> None:
    layout.addWidget(_section("FTabWidget", "路径：forza_ui/navigation/tab_widget.py | 标准标签页"))
    tabs = FTabWidget()
    tabs.addTab(FLabel("第一个标签页内容"), "概览")
    tabs.addTab(FLabel("第二个标签页内容"), "详情")
    tabs.setMaximumHeight(120)
    layout.addWidget(tabs)

    # --- FLineTabWidget：下划线风格标签 ---
    layout.addWidget(_section(
        "FLineTabWidget",
        "路径：forza_ui/navigation/line_tab_widget.py | add_tab(widget, {text, svg})",
    ))
    line_tab = FLineTabWidget()
    line_tab.add_tab(FLabel("资产列表区域"), {"text": "资产", "svg": "folder_line.svg"})
    line_tab.add_tab(FLabel("镜头列表区域"), {"text": "镜头", "svg": "media_line.svg"})
    line_tab.tool_button_group.set_fui_checked(0)
    line_tab.setMaximumHeight(140)
    layout.addWidget(line_tab)

    # --- FMenuTabWidget：图标块导航 ---
    layout.addWidget(_section("FMenuTabWidget", "路径：forza_ui/navigation/menu_tab_widget.py"))
    menu_tab = FMenuTabWidget()
    menu_tab.add_menu({"text": "首页", "svg": "home_line.svg"}, index=0)
    menu_tab.add_menu({"text": "设置", "svg": "edit_line.svg"}, index=1)
    menu_tab.tool_button_group.set_fui_checked(0)
    menu_tab_status = FLabel("当前选中：首页")
    menu_tab.tool_button_group.sig_checked_changed.connect(
        lambda idx: menu_tab_status.setText(f"当前选中：{'首页' if idx == 0 else '设置'}")
    )
    layout.addWidget(menu_tab)
    layout.addWidget(menu_tab_status)

    # --- FCollapse：手风琴折叠 ---
    layout.addWidget(_section(
        "FCollapse",
        "路径：forza_ui/navigation/collapse.py | add_section_list([{title, widget, expand}])",
    ))
    collapse = FCollapse()
    collapse.add_section_list([
        {"title": "基本信息", "expand": True, "widget": FLabel("姓名、邮箱等字段放这里")},
        {"title": "高级选项", "expand": False, "widget": FCheckBox("启用实验功能")},
        {"title": "高级选项2", "expand": False, "widget": FCheckBox("启用实验功能222")}
    ])
    layout.addWidget(collapse)

    # --- FMenu：右键/弹出菜单 ---
    layout.addWidget(_section("FMenu", "路径：forza_ui/navigation/menu.py"))
    menu_btn = FPushButton("打开菜单")
    menu = FMenu(parent=host)
    menu.addAction("新建")
    menu.addAction("打开")
    menu.addSeparator()
    menu.addAction("退出")
    menu_btn.clicked.connect(
        lambda: menu.exec_(menu_btn.mapToGlobal(menu_btn.rect().bottomLeft()))
    )
    layout.addWidget(menu_btn)

    # --- FDrawer：侧滑抽屉 ---
    layout.addWidget(_section(
        "FDrawer",
        "路径：forza_ui/navigation/drawer.py | parent 传主窗口，调用 .show() 滑出",
    ))
    drawer_btn = FPushButton("打开右侧抽屉").primary()
    drawer = FDrawer("详情面板", parent=host).right()
    drawer.set_widget(FLabel("抽屉内容：适合放筛选器、详情表单等。"))
    drawer_btn.clicked.connect(drawer.toggle)
    layout.addWidget(drawer_btn)
    host._demo_drawer = drawer  # 保持引用，防止被 GC


# ---------------------------------------------------------------------------
# 5. feedback — 反馈与状态
# ---------------------------------------------------------------------------

def _build_feedback_page(layout: QtWidgets.QVBoxLayout, host: QtWidgets.QWidget) -> None:
    layout.addWidget(_section(
        "FAlert",
        "路径：forza_ui/feedback/alert.py | 页面内嵌提示，.info()/.success()/.warning()/.error()",
    ))
    layout.addWidget(FAlert("这是一条 info 提示").info())
    layout.addWidget(FAlert("操作成功").success())
    layout.addWidget(FAlert("请注意检查").warning())
    layout.addWidget(FAlert("发生错误").error().closable())

    layout.addWidget(_section("FProgressBar / FProgressCircle", "路径：forza_ui/feedback/"))
    bar = FProgressBar()
    bar.setValue(65)
    layout.addWidget(bar)

    circle_row = QtWidgets.QHBoxLayout()
    circle = FProgressCircle()
    circle.setValue(75)
    circle_row.addWidget(circle)
    dashboard = FProgressCircle(dashboard=True)
    dashboard.setValue(60)
    circle_row.addWidget(dashboard)
    circle_wrap = QtWidgets.QWidget()
    circle_wrap.setLayout(circle_row)
    layout.addWidget(circle_wrap)

    layout.addWidget(_section(
        "FLoading / FLoadingWrapper",
        "路径：forza_ui/feedback/loading.py | Wrapper 给任意控件加加载遮罩",
    ))
    loading_row = QtWidgets.QHBoxLayout()
    loading_row.addWidget(FLoading.medium())
    wrapper_target = FPushButton("被包裹的按钮")
    wrapper = FLoadingWrapper(wrapper_target)
    toggle_loading = FPushButton("切换 Loading")
    toggle_loading.clicked.connect(lambda: wrapper.set_fui_loading(not wrapper.get_fui_loading()))
    loading_row.addWidget(wrapper)
    loading_row.addWidget(toggle_loading)
    loading_wrap = QtWidgets.QWidget()
    loading_wrap.setLayout(loading_row)
    layout.addWidget(loading_wrap)

    # FMessage / FToast：需要 parent 窗口，用按钮触发
    layout.addWidget(_section(
        "FMessage / FToast",
        "路径：forza_ui/feedback/message.py & toast.py | 类方法弹出，需传 parent 窗口",
    ))
    msg_row = QtWidgets.QHBoxLayout()
    for label, factory in [
        ("Message Info", lambda: FMessage.info("顶部消息", host)),
        ("Message OK", lambda: FMessage.success("保存成功", host)),
        ("Toast Info", lambda: FToast.info("居中 Toast", host)),
        ("Toast OK", lambda: FToast.success("完成", host)),
    ]:
        btn = FPushButton(label)
        btn.clicked.connect(factory)
        msg_row.addWidget(btn)
    msg_wrap = QtWidgets.QWidget()
    msg_wrap.setLayout(msg_row)
    layout.addWidget(msg_wrap)


# ---------------------------------------------------------------------------
# 6. layout — 布局与容器
# ---------------------------------------------------------------------------

def _build_layout_page(layout: QtWidgets.QVBoxLayout) -> None:
    layout.addWidget(_section(
        "FFlowLayout",
        "路径：forza_ui/layout/flow_layout.py | 流式布局，宽度不够时自动换行",
    ))
    flow_host = QtWidgets.QWidget()
    flow = FFlowLayout(flow_host, margin=4, spacing=8)
    for i in range(8):
        flow.addWidget(FPushButton(f"Tag {i + 1}").small())
    flow_host.setLayout(flow)
    layout.addWidget(flow_host)

    layout.addWidget(_section(
        "FSplitter",
        "路径：forza_ui/layout/splitter.py | 可拖拽分割左右/上下面板",
    ))
    splitter = FSplitter(QtCore.Qt.Horizontal)
    left = FLabel("左侧面板\n拖拽中间分隔条调整比例")
    left.setAlignment(QtCore.Qt.AlignCenter)
    right = FLabel("右侧面板")
    right.setAlignment(QtCore.Qt.AlignCenter)
    splitter.addWidget(left)
    splitter.addWidget(right)
    splitter.setMinimumHeight(100)
    layout.addWidget(splitter)


# ---------------------------------------------------------------------------
# 主窗口
# ---------------------------------------------------------------------------

class ShowcaseWindow(QtWidgets.QMainWindow):
    """
    左侧列表 = forza_ui 目录分类
    右侧     = 对应分类的全部组件演示
    """

    PAGES = [
        ("basic · 基础展示", _build_basic_page),
        ("input · 输入操作", _build_input_page),
        ("display · 数据展示", _build_display_page),
        ("navigation · 导航结构", None),  # 需要 host 引用，特殊处理
        ("feedback · 反馈状态", None),
        ("layout · 布局容器", _build_layout_page),
    ]

    def __init__(self):
        super().__init__()
        self.setWindowTitle("forza_ui 全组件学习示例")
        self.resize(1100, 720)

        self._list = QtWidgets.QListWidget()
        self._list.setFixedWidth(200)
        self._stack = QtWidgets.QStackedWidget()

        for title, _ in self.PAGES:
            self._list.addItem(title)

        # 普通页面
        self._stack.addWidget(_scroll_page(_build_basic_page))
        self._stack.addWidget(_scroll_page(_build_input_page))
        self._stack.addWidget(_scroll_page(_build_display_page))

        # navigation / feedback 需要 self 作为 parent 传给 FMenu、FMessage 等
        nav_inner = QtWidgets.QWidget()
        nav_inner.setLayout(QtWidgets.QVBoxLayout())
        _build_navigation_page(nav_inner.layout(), self)
        nav_inner.layout().addStretch()
        nav_scroll = QtWidgets.QScrollArea()
        nav_scroll.setWidgetResizable(True)
        nav_scroll.setFrameShape(QtWidgets.QFrame.NoFrame)
        nav_scroll.setWidget(nav_inner)
        self._stack.addWidget(nav_scroll)

        fb_inner = QtWidgets.QWidget()
        fb_inner.setLayout(QtWidgets.QVBoxLayout())
        _build_feedback_page(fb_inner.layout(), self)
        fb_inner.layout().addStretch()
        fb_scroll = QtWidgets.QScrollArea()
        fb_scroll.setWidgetResizable(True)
        fb_scroll.setFrameShape(QtWidgets.QFrame.NoFrame)
        fb_scroll.setWidget(fb_inner)
        self._stack.addWidget(fb_scroll)

        self._stack.addWidget(_scroll_page(_build_layout_page))

        self._list.currentRowChanged.connect(self._stack.setCurrentIndex)
        self._list.setCurrentRow(0)

        # 顶栏提示
        header = FLabel("forza_ui 组件学习示例 — 左侧切换分类，右侧查看用法").secondary()
        header.setContentsMargins(12, 8, 12, 0)

        body = QtWidgets.QWidget()
        body_lay = QtWidgets.QHBoxLayout(body)
        body_lay.setContentsMargins(0, 0, 0, 0)
        body_lay.addWidget(self._list)
        body_lay.addWidget(FDivider().vertical(), 0)
        body_lay.addWidget(self._stack, 1)

        central = QtWidgets.QWidget()
        central_lay = QtWidgets.QVBoxLayout(central)
        central_lay.setContentsMargins(0, 0, 0, 0)
        central_lay.addWidget(header)
        central_lay.addWidget(body)
        self.setCentralWidget(central)

        # 主题切换（演示 forza_theme 用法）
        theme_btn = FPushButton("切换主题")
        theme_btn.clicked.connect(self._toggle_theme)
        self.statusBar().addPermanentWidget(theme_btn)
        self._current_theme = "dark"

    def _toggle_theme(self) -> None:
        """forza_theme.set_theme() + apply() 刷新整窗样式。"""
        self._current_theme = "light" if self._current_theme == "dark" else "dark"
        forza_theme.set_theme(self._current_theme)
        forza_theme.apply(self)
        self.statusBar().showMessage(f"已切换为 {self._current_theme} 主题", 2000)


def main() -> None:
    # application() 是 forza_ui 提供的 QApplication 上下文管理器
    with application() as app:
        window = ShowcaseWindow()
        # 必须 apply 主题，否则 QSS 样式不会生效
        forza_theme.apply(window)
        window.show()
        if QtWidgets.QApplication.instance() is app:
            app.exec()


if __name__ == "__main__":
    main()
