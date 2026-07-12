# Python script to generate the massive, fully-featured WindUI_Ultimate.lua
import os

code_parts = []

# PART 1: Header, Virtual Environment Setup, and Utility Signals
code_parts.append("""--[[
================================================================================
    WindUI Ultimate v2.0 - All-In-One Roblox Luau UI Library & Key System
================================================================================
    Features:
    - Sleek Glassmorphic & Acrylic aesthetic inspired by WindUI & FluentPro
    - 23+ Custom & Built-in Themes (AMOLED, Blood Red, Cyanic, Wind Dark, Amethyst, etc.)
    - Built-in External Key System (customizable Key, URL, Note, SaveKey, Verification)
    - Sidebar Navigation with Accordion Category Folders ("DropDown Di Samping")
    - Automatic Sidebar & Content Scrolling when features exceed screen height
    - Draggable Window with Smooth Minimize to Floating Draggable Pill / Circle Icon
    - Comprehensive UI Elements (Button, Toggle, Slider, Dropdown, Colorpicker, Keybind,
      Input, Paragraph, CodeBlock, ProgressBar, Viewport 3D, Discord Banner, Media, etc.)
    - SaveManager, InterfaceManager, FloatingButtonManager, and MediaManager
    - Physics Engine (Flipper Spring/Linear Motors) & Dynamic Shine/RGB Animations
================================================================================
--]]

local WindUI = {
    Version = "2.0.0 Ultimate",
    Name = "WindUI",
    OpenFrames = {},
    Options = {},
    Themes = {},
    ThemeObjects = {},
    Window = nil,
    Unloaded = false,
    Theme = "Blood Red",
    FischBypass = (game and game.GameId == 5750914919) or false,
    DialogOpen = false,
    UseAcrylic = true,
    Transparency = true,
    MinimizeKey = Enum.KeyCode.LeftControl,
    MinimizeKeybind = nil,
    GUI = nil,
    ScrollGUI = nil,
    PopupGUI = nil,
    KeySystemGUI = nil,
    ErrorHandler = nil,
    ShineEnabled = true,
    WindowTransparent = false,
    _SBOverlays = {},
    _SBOverlayTeardowns = {},
    _ManagerDropdowns = {},
}

local Services = {
    Workspace = game:GetService("Workspace"),
    RunService = game:GetService("RunService"),
    Players = game:GetService("Players"),
    UserInputService = game:GetService("UserInputService"),
    TweenService = game:GetService("TweenService"),
    HttpService = game:GetService("HttpService"),
    TextService = game:GetService("TextService"),
    CoreGui = game:GetService("CoreGui"),
    Lighting = game:GetService("Lighting"),
    Debris = game:GetService("Debris"),
}

local LocalPlayer = Services.Players.LocalPlayer
local Mouse = LocalPlayer and LocalPlayer:GetMouse() or nil
local Camera = Services.Workspace.CurrentCamera

local protectgui = protectgui or (syn and syn.protect_gui) or function() end

-- Ensure GUI containers exist
local function SetupGUIContainers()
    if WindUI.GUI then return end
    local parent = (Services.RunService:IsStudio() and LocalPlayer and LocalPlayer:FindFirstChildOfClass("PlayerGui")) or Services.CoreGui
    
    local gui = Instance.new("ScreenGui")
    gui.Name = "WindUI_Ultimate_Main"
    gui.ResetOnSpawn = false
    gui.DisplayOrder = 10
    gui.ZIndexBehavior = Enum.ZIndexBehavior.Sibling
    protectgui(gui)
    gui.Parent = parent
    WindUI.GUI = gui

    local scrollGui = Instance.new("ScreenGui")
    scrollGui.Name = "WindUI_Ultimate_Scroll"
    scrollGui.ResetOnSpawn = false
    scrollGui.DisplayOrder = 50
    scrollGui.ZIndexBehavior = Enum.ZIndexBehavior.Sibling
    protectgui(scrollGui)
    scrollGui.Parent = parent
    WindUI.ScrollGUI = scrollGui

    local popupGui = Instance.new("ScreenGui")
    popupGui.Name = "WindUI_Ultimate_Popup"
    popupGui.ResetOnSpawn = false
    popupGui.DisplayOrder = 999
    popupGui.ZIndexBehavior = Enum.ZIndexBehavior.Sibling
    protectgui(popupGui)
    popupGui.Parent = parent
    WindUI.PopupGUI = popupGui
    
    local keyGui = Instance.new("ScreenGui")
    keyGui.Name = "WindUI_Ultimate_KeySystem"
    keyGui.ResetOnSpawn = false
    keyGui.DisplayOrder = 1000
    keyGui.ZIndexBehavior = Enum.ZIndexBehavior.Sibling
    protectgui(keyGui)
    keyGui.Parent = parent
    WindUI.KeySystemGUI = keyGui
end

SetupGUIContainers()

function WindUI.SetErrorHandler(handler)
    WindUI.ErrorHandler = handler
end

function WindUI.SafeCallback(fn, ...)
    if not fn then return end
    local ok, result = pcall(fn, ...)
    if not ok then
        local pos, errEnd = result:find(":%d+: ")
        local msg = errEnd and result:sub(errEnd + 1) or result
        if WindUI.ErrorHandler then
            pcall(WindUI.ErrorHandler, msg, result)
        end
        pcall(function()
            if WindUI.Notify then
                WindUI:Notify({ Title = "Callback Error", Content = msg, Type = "Error", Duration = 6 })
            end
        end)
    end
end

function WindUI.Round(val, decimals)
    if decimals == 0 or not decimals then
        return math.floor(val + 0.5)
    end
    local mult = 10 ^ decimals
    return math.floor(val * mult + 0.5) / mult
end

--[[
================================================================================
    Signal Module
================================================================================
--]]
local Signal = {}
Signal.__index = Signal

function Signal.new()
    return setmetatable({ _connections = {}, _threads = {} }, Signal)
end

function Signal:Connect(handler)
    local conn = {
        connected = true,
        _handler = handler,
        Disconnect = function(selfConn)
            if selfConn.connected then
                selfConn.connected = false
                for i, c in ipairs(self._connections) do
                    if c == selfConn then
                        table.remove(self._connections, i)
                        break
                    end
                end
            end
        end
    }
    table.insert(self._connections, conn)
    return conn
end
Signal.connect = Signal.Connect

function Signal:Fire(...)
    for _, conn in ipairs(self._connections) do
        if conn.connected and conn._handler then
            task.spawn(conn._handler, ...)
        end
    end
    for _, thread in ipairs(self._threads) do
        coroutine.resume(thread, ...)
    end
    self._threads = {}
end
Signal.fire = Signal.Fire

function Signal:Wait()
    table.insert(self._threads, coroutine.running())
    return coroutine.yield()
end
Signal.wait = Signal.Wait
""")

print("Part 1 added.")

# PART 2: Physics & Flipper Engine + UI Creator Utility
code_parts.append("""
--[[
================================================================================
    Physics & Flipper Engine (Spring, Linear, Instant, Motors)
================================================================================
--]]
local Physics = {}

-- Instant
local Instant = {}
Instant.__index = Instant
function Instant.new(targetValue)
    return setmetatable({ _targetValue = targetValue }, Instant)
end
function Instant:step()
    return { complete = true, value = self._targetValue }
end
Physics.Instant = Instant

-- Linear
local Linear = {}
Linear.__index = Linear
function Linear.new(targetValue, options)
    options = options or {}
    return setmetatable({ _targetValue = targetValue, _velocity = options.velocity or 1 }, Linear)
end
function Linear:step(state, dt)
    local cur, vel, target = state.value, self._velocity, self._targetValue
    local delta = dt * vel
    local complete = delta >= math.abs(target - cur)
    cur = cur + delta * (target > cur and 1 or -1)
    if complete then
        cur = target
        vel = 0
    end
    return { complete = complete, value = cur, velocity = vel }
end
Physics.Linear = Linear

-- Spring
local Spring = {}
Spring.__index = Spring
function Spring.new(targetValue, options)
    options = options or {}
    return setmetatable({
        _targetValue = targetValue,
        _frequency = options.frequency or 4,
        _dampingRatio = options.dampingRatio or 1
    }, Spring)
end
function Spring:step(state, dt)
    local d, f, t, cur, vel = self._dampingRatio, self._frequency * 2 * math.pi, self._targetValue, state.value, state.velocity or 0
    local offset = cur - t
    local decay = math.exp(-d * f * dt)
    local newPos, newVel
    if d == 1 then
        newPos = (offset * (1 + f * dt) + vel * dt) * decay + t
        newVel = (vel * (1 - f * dt) - offset * (f * f * dt)) * decay
    elseif d < 1 then
        local c = math.sqrt(1 - d * d)
        local cosV, sinV = math.cos(f * c * dt), math.sin(f * c * dt)
        local term
        if c > 0.0001 then
            term = sinV / c
        else
            term = dt * f
        end
        newPos = (offset * (cosV + d * term) + vel * (sinV / (f * (c > 0.0001 and c or 1)))) * decay + t
        newVel = (vel * (cosV - term * d) - offset * (term * f)) * decay
    else
        local c = math.sqrt(d * d - 1)
        local r1, r2 = -f * (d - c), -f * (d + c)
        local co2 = (vel - offset * r1) / (2 * f * c)
        local co1 = offset - co2
        local e1, e2 = co1 * math.exp(r1 * dt), co2 * math.exp(r2 * dt)
        newPos = e1 + e2 + t
        newVel = e1 * r1 + e2 * r2
    end
    local complete = math.abs(newVel) < 0.001 and math.abs(newPos - t) < 0.001
    return { complete = complete, value = complete and t or newPos, velocity = newVel }
end
Physics.Spring = Spring

-- BaseMotor
local BaseMotor = {}
BaseMotor.__index = BaseMotor
function BaseMotor.new()
    return setmetatable({
        _onStep = Signal.new(),
        _onStart = Signal.new(),
        _onComplete = Signal.new()
    }, BaseMotor)
end
function BaseMotor:OnStep(fn) return self._onStep:Connect(fn) end
function BaseMotor:OnStart(fn) return self._onStart:Connect(fn) end
function BaseMotor:OnComplete(fn) return self._onComplete:Connect(fn) end
function BaseMotor:Start()
    if not self._connection then
        self._connection = Services.RunService.RenderStepped:Connect(function(dt)
            self:step(dt)
        end)
    end
end
function BaseMotor:Stop()
    if self._connection then
        self._connection:Disconnect()
        self._connection = nil
    end
end
function BaseMotor:Destroy() self:Stop() end
Physics.BaseMotor = BaseMotor

-- SingleMotor
local SingleMotor = setmetatable({}, BaseMotor)
SingleMotor.__index = SingleMotor
function SingleMotor.new(initialValue, useImplicitConnections)
    local self = setmetatable(BaseMotor.new(), SingleMotor)
    self._useImplicitConnections = (useImplicitConnections ~= false)
    self._goal = nil
    self._state = { complete = true, value = initialValue }
    return self
end
function SingleMotor:step(dt)
    if self._state.complete then return true end
    local newState = self._goal:step(self._state, dt)
    self._state = newState
    self._onStep:Fire(newState.value)
    if newState.complete then
        if self._useImplicitConnections then self:Stop() end
        self._onComplete:Fire()
    end
    return newState.complete
end
function SingleMotor:GetValue() return self._state.value end
function SingleMotor:SetGoal(goal)
    self._state.complete = false
    self._goal = goal
    self._onStart:Fire()
    if self._useImplicitConnections then self:Start() end
end
Physics.SingleMotor = SingleMotor

-- GroupMotor
local GroupMotor = setmetatable({}, BaseMotor)
GroupMotor.__index = GroupMotor
function GroupMotor.new(initialValues, useImplicitConnections)
    local self = setmetatable(BaseMotor.new(), GroupMotor)
    self._useImplicitConnections = (useImplicitConnections ~= false)
    self._complete = true
    self._motors = {}
    for k, v in pairs(initialValues) do
        if type(v) == "number" then
            self._motors[k] = SingleMotor.new(v, false)
        elseif type(v) == "table" and v.step then
            self._motors[k] = v
        end
    end
    return self
end
function GroupMotor:step(dt)
    if self._complete then return true end
    local allComplete = true
    for _, motor in pairs(self._motors) do
        if not motor:step(dt) then allComplete = false end
    end
    self._onStep:Fire(self:GetValue())
    if allComplete then
        if self._useImplicitConnections then self:Stop() end
        self._complete = true
        self._onComplete:Fire()
    end
    return allComplete
end
function GroupMotor:GetValue()
    local res = {}
    for k, motor in pairs(self._motors) do res[k] = motor:GetValue() end
    return res
end
function GroupMotor:SetGoal(goals)
    self._complete = false
    self._onStart:Fire()
    for k, goal in pairs(goals) do
        if self._motors[k] then self._motors[k]:SetGoal(goal) end
    end
    if self._useImplicitConnections then self:Start() end
end
Physics.GroupMotor = GroupMotor
WindUI.Physics = Physics

--[[
================================================================================
    UI Creator & Theme Tag Utility
================================================================================
--]]
local Creator = {}
Creator.__index = Creator

function Creator.New(className, properties, children)
    local instance = Instance.new(className)
    if properties then
        for k, v in pairs(properties) do
            if k == "ThemeTag" and type(v) == "table" then
                Creator.AddThemeObject(instance, v)
            elseif k == "Parent" then
                instance.Parent = v
            else
                pcall(function() instance[k] = v end)
            end
        end
    end
    if children then
        for _, child in ipairs(children) do
            if child and typeof(child) == "Instance" then
                child.Parent = instance
            end
        end
    end
    return instance
end

function Creator.AddSignal(signal, handler)
    if signal and handler then
        return signal:Connect(handler)
    end
end

function Creator.AddThemeObject(instance, propertiesMap)
    WindUI.ThemeObjects[instance] = propertiesMap
    Creator.UpdateThemeForInstance(instance, propertiesMap)
end

function Creator.UpdateThemeForInstance(instance, propertiesMap)
    local themeData = WindUI.Themes[WindUI.Theme] or WindUI.Themes["Blood Red"] or {}
    if not instance or not instance.Parent then return end
    for prop, themeKey in pairs(propertiesMap) do
        local val = themeData[themeKey]
        if val ~= nil then
            pcall(function() instance[prop] = val end)
        end
    end
end

function Creator.UpdateTheme()
    for instance, propMap in pairs(WindUI.ThemeObjects) do
        if instance and instance.Parent then
            Creator.UpdateThemeForInstance(instance, propMap)
        else
            WindUI.ThemeObjects[instance] = nil
        end
    end
end

function Creator.SpringMotor(initialValue, instance, property)
    local motor = SingleMotor.new(initialValue, true)
    motor:OnStep(function(val)
        if instance and instance.Parent then
            pcall(function() instance[property] = val end)
        end
    end)
    return motor, function(goalVal)
        motor:SetGoal(Spring.new(goalVal, { frequency = 6, dampingRatio = 0.9 }))
    end
end

WindUI.Creator = Creator
""")
print("Part 2 added.")

# PART 3: 23+ Themes & Shine/RGB Animation Engine
code_parts.append("""
--[[
================================================================================
    23+ Themes Definitions & Shine / RGB Animation Engine
================================================================================
--]]
local Themes = {
    ["Blood Red"] = {
        Name = "Blood Red", Accent = Color3.fromRGB(180, 10, 20),
        AcrylicMain = Color3.fromRGB(35, 8, 10), AcrylicBorder = Color3.fromRGB(140, 15, 25),
        AcrylicGradient = ColorSequence.new(Color3.fromRGB(130, 12, 20), Color3.fromRGB(28, 5, 8)),
        AcrylicNoise = 0.9, TitleBarLine = Color3.fromRGB(155, 18, 28),
        Tab = Color3.fromRGB(145, 15, 25), Element = Color3.fromRGB(130, 12, 22),
        ElementBorder = Color3.fromRGB(85, 8, 14), InElementBorder = Color3.fromRGB(150, 18, 28),
        ElementTransparency = 0.88, ToggleSlider = Color3.fromRGB(180, 10, 20),
        ToggleToggled = Color3.fromRGB(255, 230, 230), SliderRail = Color3.fromRGB(145, 15, 25),
        DropdownFrame = Color3.fromRGB(115, 10, 18), DropdownHolder = Color3.fromRGB(28, 5, 8),
        DropdownBorder = Color3.fromRGB(80, 7, 13), DropdownOption = Color3.fromRGB(180, 10, 20),
        Keybind = Color3.fromRGB(130, 12, 22), Input = Color3.fromRGB(115, 10, 18),
        InputFocused = Color3.fromRGB(18, 3, 5), InputIndicator = Color3.fromRGB(220, 50, 70),
        Dialog = Color3.fromRGB(28, 5, 8), DialogHolder = Color3.fromRGB(18, 3, 5),
        DialogHolderLine = Color3.fromRGB(12, 2, 3), DialogButton = Color3.fromRGB(28, 5, 8),
        DialogButtonBorder = Color3.fromRGB(145, 15, 25), DialogBorder = Color3.fromRGB(85, 8, 14),
        DialogInput = Color3.fromRGB(50, 10, 14), DialogInputLine = Color3.fromRGB(220, 50, 70),
        Text = Color3.fromRGB(255, 230, 230), SubText = Color3.fromRGB(210, 175, 178),
        Hover = Color3.fromRGB(180, 10, 20), HoverChange = 0.05, ShineEnabled = true,
        Shine = { Speed = 0.5, RotationSpeed = 25, ColorSequence = ColorSequence.new({ ColorSequenceKeypoint.new(0, Color3.fromRGB(71, 0, 0)), ColorSequenceKeypoint.new(0.5, Color3.fromRGB(180, 10, 20)), ColorSequenceKeypoint.new(1, Color3.fromRGB(71, 0, 0)) }) },
        StrokeShine = true, StrokeDark = Color3.fromRGB(145, 15, 25),
        Background = "rbxassetid://121343473918667", BackgroundTransparency = 0.15,
        ThemeAccentColors = { Color3.fromRGB(180, 10, 20) },
    },
    ["AMOLED"] = {
        Name = "AMOLED", Accent = Color3.fromRGB(255, 255, 255),
        AcrylicMain = Color3.fromRGB(0, 0, 0), AcrylicBorder = Color3.fromRGB(25, 25, 25),
        AcrylicGradient = ColorSequence.new(Color3.fromRGB(0, 0, 0), Color3.fromRGB(0, 0, 0)),
        AcrylicNoise = 0.98, TitleBarLine = Color3.fromRGB(22, 22, 22),
        Tab = Color3.fromRGB(28, 28, 28), Element = Color3.fromRGB(10, 10, 10),
        ElementBorder = Color3.fromRGB(20, 20, 20), InElementBorder = Color3.fromRGB(30, 30, 30),
        ElementTransparency = 0.95, ToggleSlider = Color3.fromRGB(40, 40, 40),
        ToggleToggled = Color3.fromRGB(255, 255, 255), SliderRail = Color3.fromRGB(30, 30, 30),
        DropdownFrame = Color3.fromRGB(18, 18, 18), DropdownHolder = Color3.fromRGB(0, 0, 0),
        DropdownBorder = Color3.fromRGB(25, 25, 25), DropdownOption = Color3.fromRGB(255, 255, 255),
        Keybind = Color3.fromRGB(22, 22, 22), Input = Color3.fromRGB(12, 12, 12),
        InputFocused = Color3.fromRGB(0, 0, 0), InputIndicator = Color3.fromRGB(255, 255, 255),
        Dialog = Color3.fromRGB(6, 6, 6), DialogHolder = Color3.fromRGB(0, 0, 0),
        DialogHolderLine = Color3.fromRGB(18, 18, 18), DialogButton = Color3.fromRGB(10, 10, 10),
        DialogButtonBorder = Color3.fromRGB(28, 28, 28), DialogBorder = Color3.fromRGB(22, 22, 22),
        DialogInput = Color3.fromRGB(10, 10, 10), DialogInputLine = Color3.fromRGB(45, 45, 45),
        Text = Color3.fromRGB(255, 255, 255), SubText = Color3.fromRGB(160, 160, 160),
        Hover = Color3.fromRGB(255, 255, 255), HoverChange = 0.04, ShineEnabled = false,
        StrokeShine = false, StrokeDark = Color3.fromRGB(18, 18, 18),
        Background = "rbxassetid://134736124666311", BackgroundTransparency = 0,
        ThemeAccentColors = { Color3.fromRGB(255, 255, 255) },
    },
    ["RGB"] = {
        Name = "RGB", Accent = Color3.fromRGB(0, 255, 180),
        AcrylicMain = Color3.fromRGB(8, 8, 14), AcrylicBorder = Color3.fromRGB(0, 255, 180),
        AcrylicGradient = ColorSequence.new({ ColorSequenceKeypoint.new(0, Color3.fromRGB(20, 0, 40)), ColorSequenceKeypoint.new(0.5, Color3.fromRGB(0, 20, 50)), ColorSequenceKeypoint.new(1, Color3.fromRGB(30, 0, 30)) }),
        AcrylicNoise = 0.95, TitleBarLine = Color3.fromRGB(0, 200, 140),
        Tab = Color3.fromRGB(0, 200, 160), Element = Color3.fromRGB(20, 20, 35),
        ElementBorder = Color3.fromRGB(10, 10, 20), InElementBorder = Color3.fromRGB(0, 200, 160),
        ElementTransparency = 0.88, ToggleSlider = Color3.fromRGB(0, 180, 140),
        ToggleToggled = Color3.fromRGB(0, 0, 0), SliderRail = Color3.fromRGB(0, 200, 160),
        DropdownFrame = Color3.fromRGB(0, 200, 160), DropdownHolder = Color3.fromRGB(8, 8, 20),
        DropdownBorder = Color3.fromRGB(0, 200, 160), DropdownOption = Color3.fromRGB(0, 200, 160),
        Keybind = Color3.fromRGB(0, 200, 160), Input = Color3.fromRGB(20, 20, 40),
        InputFocused = Color3.fromRGB(5, 5, 12), InputIndicator = Color3.fromRGB(0, 180, 140),
        Dialog = Color3.fromRGB(8, 8, 20), DialogHolder = Color3.fromRGB(5, 5, 15),
        DialogHolderLine = Color3.fromRGB(0, 200, 160), DialogButton = Color3.fromRGB(10, 10, 22),
        DialogButtonBorder = Color3.fromRGB(0, 200, 160), DialogBorder = Color3.fromRGB(0, 200, 160),
        DialogInput = Color3.fromRGB(15, 15, 30), DialogInputLine = Color3.fromRGB(0, 200, 160),
        Text = Color3.fromRGB(220, 255, 245), SubText = Color3.fromRGB(100, 220, 190),
        Hover = Color3.fromRGB(0, 255, 180), HoverChange = 0.05, ShineEnabled = true,
        Shine = { Speed = 1.2, RotationSpeed = 40, ColorSequence = ColorSequence.new({ ColorSequenceKeypoint.new(0, Color3.fromRGB(0, 255, 180)), ColorSequenceKeypoint.new(0.33, Color3.fromRGB(120, 0, 255)), ColorSequenceKeypoint.new(0.66, Color3.fromRGB(255, 0, 150)), ColorSequenceKeypoint.new(1, Color3.fromRGB(0, 255, 180)) }) },
        StrokeShine = true, StrokeDark = Color3.fromRGB(0, 180, 140), IsRGB = true,
        ThemeAccentColors = { Color3.fromRGB(0, 255, 180), Color3.fromRGB(120, 0, 255), Color3.fromRGB(255, 0, 150) },
    },
    ["Wind Dark"] = {
        Name = "Wind Dark", Accent = Color3.fromRGB(90, 165, 255),
        AcrylicMain = Color3.fromRGB(14, 16, 22), AcrylicBorder = Color3.fromRGB(45, 60, 95),
        AcrylicGradient = ColorSequence.new(Color3.fromRGB(18, 22, 34), Color3.fromRGB(10, 12, 18)),
        AcrylicNoise = 0.94, TitleBarLine = Color3.fromRGB(40, 55, 85),
        Tab = Color3.fromRGB(60, 120, 220), Element = Color3.fromRGB(22, 26, 38),
        ElementBorder = Color3.fromRGB(32, 38, 56), InElementBorder = Color3.fromRGB(60, 120, 220),
        ElementTransparency = 0.88, ToggleSlider = Color3.fromRGB(90, 165, 255),
        ToggleToggled = Color3.fromRGB(255, 255, 255), SliderRail = Color3.fromRGB(40, 55, 85),
        DropdownFrame = Color3.fromRGB(26, 32, 48), DropdownHolder = Color3.fromRGB(12, 14, 20),
        DropdownBorder = Color3.fromRGB(45, 60, 95), DropdownOption = Color3.fromRGB(90, 165, 255),
        Keybind = Color3.fromRGB(26, 32, 48), Input = Color3.fromRGB(20, 24, 35),
        InputFocused = Color3.fromRGB(10, 12, 18), InputIndicator = Color3.fromRGB(90, 165, 255),
        Dialog = Color3.fromRGB(14, 16, 22), DialogHolder = Color3.fromRGB(10, 12, 18),
        DialogHolderLine = Color3.fromRGB(40, 55, 85), DialogButton = Color3.fromRGB(22, 26, 38),
        DialogButtonBorder = Color3.fromRGB(45, 60, 95), DialogBorder = Color3.fromRGB(45, 60, 95),
        DialogInput = Color3.fromRGB(20, 24, 35), DialogInputLine = Color3.fromRGB(90, 165, 255),
        Text = Color3.fromRGB(240, 245, 255), SubText = Color3.fromRGB(160, 175, 205),
        Hover = Color3.fromRGB(90, 165, 255), HoverChange = 0.05, ShineEnabled = true,
        Shine = { Speed = 0.6, RotationSpeed = 25, ColorSequence = ColorSequence.new({ ColorSequenceKeypoint.new(0, Color3.fromRGB(20, 40, 80)), ColorSequenceKeypoint.new(0.5, Color3.fromRGB(90, 165, 255)), ColorSequenceKeypoint.new(1, Color3.fromRGB(20, 40, 80)) }) },
        StrokeShine = true, StrokeDark = Color3.fromRGB(40, 55, 85),
        ThemeAccentColors = { Color3.fromRGB(90, 165, 255) },
    },
    ["Wind Light"] = {
        Name = "Wind Light", Accent = Color3.fromRGB(30, 120, 235),
        AcrylicMain = Color3.fromRGB(245, 247, 252), AcrylicBorder = Color3.fromRGB(190, 205, 230),
        AcrylicGradient = ColorSequence.new(Color3.fromRGB(255, 255, 255), Color3.fromRGB(235, 240, 248)),
        AcrylicNoise = 0.95, TitleBarLine = Color3.fromRGB(210, 220, 240),
        Tab = Color3.fromRGB(30, 120, 235), Element = Color3.fromRGB(255, 255, 255),
        ElementBorder = Color3.fromRGB(215, 225, 242), InElementBorder = Color3.fromRGB(160, 190, 240),
        ElementTransparency = 0.82, ToggleSlider = Color3.fromRGB(30, 120, 235),
        ToggleToggled = Color3.fromRGB(255, 255, 255), SliderRail = Color3.fromRGB(200, 215, 240),
        DropdownFrame = Color3.fromRGB(245, 248, 255), DropdownHolder = Color3.fromRGB(255, 255, 255),
        DropdownBorder = Color3.fromRGB(190, 205, 230), DropdownOption = Color3.fromRGB(30, 120, 235),
        Keybind = Color3.fromRGB(235, 242, 255), Input = Color3.fromRGB(255, 255, 255),
        InputFocused = Color3.fromRGB(240, 245, 255), InputIndicator = Color3.fromRGB(30, 120, 235),
        Dialog = Color3.fromRGB(255, 255, 255), DialogHolder = Color3.fromRGB(245, 247, 252),
        DialogHolderLine = Color3.fromRGB(210, 220, 240), DialogButton = Color3.fromRGB(240, 245, 255),
        DialogButtonBorder = Color3.fromRGB(190, 205, 230), DialogBorder = Color3.fromRGB(190, 205, 230),
        DialogInput = Color3.fromRGB(255, 255, 255), DialogInputLine = Color3.fromRGB(30, 120, 235),
        Text = Color3.fromRGB(25, 30, 45), SubText = Color3.fromRGB(100, 115, 145),
        Hover = Color3.fromRGB(30, 120, 235), HoverChange = 0.05, ShineEnabled = false,
        StrokeShine = false, StrokeDark = Color3.fromRGB(190, 205, 230),
        ThemeAccentColors = { Color3.fromRGB(30, 120, 235) },
    },
    ["Amethyst Glass"] = {
        Name = "Amethyst Glass", Accent = Color3.fromRGB(165, 85, 245),
        AcrylicMain = Color3.fromRGB(20, 12, 30), AcrylicBorder = Color3.fromRGB(110, 60, 175),
        AcrylicGradient = ColorSequence.new(Color3.fromRGB(35, 18, 55), Color3.fromRGB(14, 8, 22)),
        AcrylicNoise = 0.93, TitleBarLine = Color3.fromRGB(90, 45, 150),
        Tab = Color3.fromRGB(165, 85, 245), Element = Color3.fromRGB(32, 18, 50),
        ElementBorder = Color3.fromRGB(65, 35, 105), InElementBorder = Color3.fromRGB(135, 70, 215),
        ElementTransparency = 0.88, ToggleSlider = Color3.fromRGB(165, 85, 245),
        ToggleToggled = Color3.fromRGB(255, 255, 255), SliderRail = Color3.fromRGB(90, 45, 150),
        DropdownFrame = Color3.fromRGB(38, 22, 60), DropdownHolder = Color3.fromRGB(16, 9, 25),
        DropdownBorder = Color3.fromRGB(90, 45, 150), DropdownOption = Color3.fromRGB(165, 85, 245),
        Keybind = Color3.fromRGB(38, 22, 60), Input = Color3.fromRGB(30, 16, 48),
        InputFocused = Color3.fromRGB(14, 8, 22), InputIndicator = Color3.fromRGB(180, 110, 255),
        Dialog = Color3.fromRGB(20, 12, 30), DialogHolder = Color3.fromRGB(14, 8, 22),
        DialogHolderLine = Color3.fromRGB(90, 45, 150), DialogButton = Color3.fromRGB(32, 18, 50),
        DialogButtonBorder = Color3.fromRGB(110, 60, 175), DialogBorder = Color3.fromRGB(110, 60, 175),
        DialogInput = Color3.fromRGB(30, 16, 48), DialogInputLine = Color3.fromRGB(180, 110, 255),
        Text = Color3.fromRGB(248, 240, 255), SubText = Color3.fromRGB(185, 165, 215),
        Hover = Color3.fromRGB(165, 85, 245), HoverChange = 0.05, ShineEnabled = true,
        Shine = { Speed = 0.5, RotationSpeed = 25, ColorSequence = ColorSequence.new({ ColorSequenceKeypoint.new(0, Color3.fromRGB(45, 20, 80)), ColorSequenceKeypoint.new(0.5, Color3.fromRGB(180, 110, 255)), ColorSequenceKeypoint.new(1, Color3.fromRGB(45, 20, 80)) }) },
        StrokeShine = true, StrokeDark = Color3.fromRGB(90, 45, 150),
        ThemeAccentColors = { Color3.fromRGB(165, 85, 245) },
    },
    ["Emerald Glass"] = {
        Name = "Emerald Glass", Accent = Color3.fromRGB(45, 215, 130),
        AcrylicMain = Color3.fromRGB(10, 24, 16), AcrylicBorder = Color3.fromRGB(35, 135, 85),
        AcrylicGradient = ColorSequence.new(Color3.fromRGB(16, 40, 26), Color3.fromRGB(6, 16, 10)),
        AcrylicNoise = 0.93, TitleBarLine = Color3.fromRGB(30, 110, 70),
        Tab = Color3.fromRGB(45, 215, 130), Element = Color3.fromRGB(18, 36, 24),
        ElementBorder = Color3.fromRGB(26, 65, 42), InElementBorder = Color3.fromRGB(45, 215, 130),
        ElementTransparency = 0.88, ToggleSlider = Color3.fromRGB(45, 215, 130),
        ToggleToggled = Color3.fromRGB(0, 0, 0), SliderRail = Color3.fromRGB(30, 110, 70),
        DropdownFrame = Color3.fromRGB(22, 44, 30), DropdownHolder = Color3.fromRGB(8, 18, 12),
        DropdownBorder = Color3.fromRGB(35, 135, 85), DropdownOption = Color3.fromRGB(45, 215, 130),
        Keybind = Color3.fromRGB(22, 44, 30), Input = Color3.fromRGB(16, 34, 22),
        InputFocused = Color3.fromRGB(6, 16, 10), InputIndicator = Color3.fromRGB(65, 235, 150),
        Dialog = Color3.fromRGB(10, 24, 16), DialogHolder = Color3.fromRGB(6, 16, 10),
        DialogHolderLine = Color3.fromRGB(30, 110, 70), DialogButton = Color3.fromRGB(18, 36, 24),
        DialogButtonBorder = Color3.fromRGB(35, 135, 85), DialogBorder = Color3.fromRGB(35, 135, 85),
        DialogInput = Color3.fromRGB(16, 34, 22), DialogInputLine = Color3.fromRGB(65, 235, 150),
        Text = Color3.fromRGB(235, 255, 245), SubText = Color3.fromRGB(150, 205, 175),
        Hover = Color3.fromRGB(45, 215, 130), HoverChange = 0.05, ShineEnabled = true,
        Shine = { Speed = 0.5, RotationSpeed = 25, ColorSequence = ColorSequence.new({ ColorSequenceKeypoint.new(0, Color3.fromRGB(15, 60, 35)), ColorSequenceKeypoint.new(0.5, Color3.fromRGB(65, 235, 150)), ColorSequenceKeypoint.new(1, Color3.fromRGB(15, 60, 35)) }) },
        StrokeShine = true, StrokeDark = Color3.fromRGB(30, 110, 70),
        ThemeAccentColors = { Color3.fromRGB(45, 215, 130) },
    },
    ["Neon Cyber"] = {
        Name = "Neon Cyber", Accent = Color3.fromRGB(57, 255, 20),
        AcrylicMain = Color3.fromRGB(5, 10, 5), AcrylicBorder = Color3.fromRGB(40, 200, 20),
        AcrylicGradient = ColorSequence.new(Color3.fromRGB(10, 25, 10), Color3.fromRGB(3, 8, 3)),
        AcrylicNoise = 0.93, TitleBarLine = Color3.fromRGB(35, 160, 15),
        Tab = Color3.fromRGB(57, 255, 20), Element = Color3.fromRGB(10, 22, 10),
        ElementBorder = Color3.fromRGB(15, 45, 15), InElementBorder = Color3.fromRGB(35, 160, 15),
        ElementTransparency = 0.88, ToggleSlider = Color3.fromRGB(57, 255, 20),
        ToggleToggled = Color3.fromRGB(0, 0, 0), SliderRail = Color3.fromRGB(57, 255, 20),
        DropdownFrame = Color3.fromRGB(35, 160, 15), DropdownHolder = Color3.fromRGB(5, 12, 5),
        DropdownBorder = Color3.fromRGB(35, 160, 15), DropdownOption = Color3.fromRGB(57, 255, 20),
        Keybind = Color3.fromRGB(40, 200, 18), Input = Color3.fromRGB(10, 22, 10),
        InputFocused = Color3.fromRGB(3, 7, 3), InputIndicator = Color3.fromRGB(57, 255, 20),
        Dialog = Color3.fromRGB(5, 12, 5), DialogHolder = Color3.fromRGB(3, 8, 3),
        DialogHolderLine = Color3.fromRGB(35, 160, 15), DialogButton = Color3.fromRGB(8, 18, 8),
        DialogButtonBorder = Color3.fromRGB(57, 255, 20), DialogBorder = Color3.fromRGB(40, 200, 18),
        DialogInput = Color3.fromRGB(10, 22, 10), DialogInputLine = Color3.fromRGB(57, 255, 20),
        Text = Color3.fromRGB(200, 255, 190), SubText = Color3.fromRGB(80, 200, 60),
        Hover = Color3.fromRGB(57, 255, 20), HoverChange = 0.05, ShineEnabled = true,
        Shine = { Speed = 0.8, RotationSpeed = 30, ColorSequence = ColorSequence.new({ ColorSequenceKeypoint.new(0, Color3.fromRGB(5, 30, 5)), ColorSequenceKeypoint.new(0.5, Color3.fromRGB(57, 255, 20)), ColorSequenceKeypoint.new(1, Color3.fromRGB(5, 30, 5)) }) },
        StrokeShine = true, StrokeDark = Color3.fromRGB(35, 160, 15),
        ThemeAccentColors = { Color3.fromRGB(57, 255, 20) },
    },
    ["Cyanic"] = {
        Name = "Cyanic", Accent = Color3.fromRGB(57, 197, 187),
        AcrylicMain = Color3.fromRGB(8, 18, 22), AcrylicBorder = Color3.fromRGB(40, 170, 165),
        AcrylicGradient = ColorSequence.new({ ColorSequenceKeypoint.new(0, Color3.fromRGB(15, 45, 55)), ColorSequenceKeypoint.new(0.5, Color3.fromRGB(8, 25, 32)), ColorSequenceKeypoint.new(1, Color3.fromRGB(4, 12, 16)) }),
        AcrylicNoise = 0.92, TitleBarLine = Color3.fromRGB(35, 155, 150),
        Tab = Color3.fromRGB(40, 165, 160), Element = Color3.fromRGB(14, 38, 46),
        ElementBorder = Color3.fromRGB(18, 50, 60), InElementBorder = Color3.fromRGB(40, 165, 160),
        ElementTransparency = 0.88, ToggleSlider = Color3.fromRGB(57, 197, 187),
        ToggleToggled = Color3.fromRGB(0, 0, 0), SliderRail = Color3.fromRGB(40, 165, 160),
        DropdownFrame = Color3.fromRGB(32, 140, 135), DropdownHolder = Color3.fromRGB(6, 18, 22),
        DropdownBorder = Color3.fromRGB(40, 165, 160), DropdownOption = Color3.fromRGB(57, 197, 187),
        Keybind = Color3.fromRGB(14, 38, 46), Input = Color3.fromRGB(10, 28, 35),
        InputFocused = Color3.fromRGB(4, 10, 14), InputIndicator = Color3.fromRGB(80, 215, 205),
        Dialog = Color3.fromRGB(8, 22, 28), DialogHolder = Color3.fromRGB(5, 14, 18),
        DialogHolderLine = Color3.fromRGB(35, 155, 150), DialogButton = Color3.fromRGB(10, 26, 32),
        DialogButtonBorder = Color3.fromRGB(40, 165, 160), DialogBorder = Color3.fromRGB(30, 120, 115),
        DialogInput = Color3.fromRGB(12, 32, 40), DialogInputLine = Color3.fromRGB(80, 215, 205),
        Text = Color3.fromRGB(210, 248, 246), SubText = Color3.fromRGB(130, 210, 205),
        Hover = Color3.fromRGB(57, 197, 187), HoverChange = 0.05, ShineEnabled = true,
        Shine = { Speed = 0.6, RotationSpeed = 25, ColorSequence = ColorSequence.new({ ColorSequenceKeypoint.new(0, Color3.fromRGB(10, 40, 50)), ColorSequenceKeypoint.new(0.5, Color3.fromRGB(57, 197, 187)), ColorSequenceKeypoint.new(1, Color3.fromRGB(10, 40, 50)) }) },
        StrokeShine = true, StrokeDark = Color3.fromRGB(35, 155, 150),
        Background = "rbxassetid://95656189244173", BackgroundTransparency = 0.12,
        ThemeAccentColors = { Color3.fromRGB(57, 197, 187) },
    },
    ["Ash Gray"] = {
        Name = "Ash Gray", Accent = Color3.fromRGB(150, 150, 150),
        AcrylicMain = Color3.fromRGB(60, 60, 60), AcrylicBorder = Color3.fromRGB(90, 90, 90),
        AcrylicGradient = ColorSequence.new(Color3.fromRGB(40, 40, 40), Color3.fromRGB(40, 40, 40)),
        AcrylicNoise = 0.9, TitleBarLine = Color3.fromRGB(75, 75, 75),
        Tab = Color3.fromRGB(120, 120, 120), Element = Color3.fromRGB(120, 120, 120),
        ElementBorder = Color3.fromRGB(45, 45, 45), InElementBorder = Color3.fromRGB(90, 90, 90),
        ElementTransparency = 0.87, ToggleSlider = Color3.fromRGB(120, 120, 120),
        ToggleToggled = Color3.fromRGB(0, 0, 0), SliderRail = Color3.fromRGB(120, 120, 120),
        DropdownFrame = Color3.fromRGB(160, 160, 160), DropdownHolder = Color3.fromRGB(45, 45, 45),
        DropdownBorder = Color3.fromRGB(90, 90, 90), DropdownOption = Color3.fromRGB(120, 120, 120),
        Keybind = Color3.fromRGB(120, 120, 120), Input = Color3.fromRGB(160, 160, 160),
        InputFocused = Color3.fromRGB(10, 10, 10), InputIndicator = Color3.fromRGB(150, 150, 150),
        Dialog = Color3.fromRGB(45, 45, 45), DialogHolder = Color3.fromRGB(35, 35, 35),
        DialogHolderLine = Color3.fromRGB(30, 30, 30), DialogButton = Color3.fromRGB(45, 45, 45),
        DialogButtonBorder = Color3.fromRGB(80, 80, 80), DialogBorder = Color3.fromRGB(70, 70, 70),
        DialogInput = Color3.fromRGB(55, 55, 55), DialogInputLine = Color3.fromRGB(160, 160, 160),
        Text = Color3.fromRGB(240, 240, 240), SubText = Color3.fromRGB(170, 170, 170),
        Hover = Color3.fromRGB(150, 150, 150), HoverChange = 0.05, ShineEnabled = false,
        StrokeShine = false, StrokeDark = Color3.fromRGB(90, 90, 90),
        ThemeAccentColors = { Color3.fromRGB(150, 150, 150) },
    },
    ["Amber Glow"] = {
        Name = "Amber Glow", Accent = Color3.fromRGB(255, 170, 40),
        AcrylicMain = Color3.fromRGB(18, 10, 4), AcrylicBorder = Color3.fromRGB(200, 130, 30),
        AcrylicGradient = ColorSequence.new({ ColorSequenceKeypoint.new(0, Color3.fromRGB(50, 25, 5)), ColorSequenceKeypoint.new(0.5, Color3.fromRGB(28, 14, 3)), ColorSequenceKeypoint.new(1, Color3.fromRGB(10, 5, 1)) }),
        AcrylicNoise = 0.9, TitleBarLine = Color3.fromRGB(185, 120, 25),
        Tab = Color3.fromRGB(190, 125, 25), Element = Color3.fromRGB(38, 20, 5),
        ElementBorder = Color3.fromRGB(60, 35, 10), InElementBorder = Color3.fromRGB(200, 130, 30),
        ElementTransparency = 0.88, ToggleSlider = Color3.fromRGB(255, 170, 40),
        ToggleToggled = Color3.fromRGB(0, 0, 0), SliderRail = Color3.fromRGB(190, 125, 25),
        DropdownFrame = Color3.fromRGB(165, 105, 20), DropdownHolder = Color3.fromRGB(14, 7, 2),
        DropdownBorder = Color3.fromRGB(200, 130, 30), DropdownOption = Color3.fromRGB(255, 170, 40),
        Keybind = Color3.fromRGB(38, 20, 5), Input = Color3.fromRGB(28, 14, 3),
        InputFocused = Color3.fromRGB(8, 4, 1), InputIndicator = Color3.fromRGB(255, 195, 80),
        Dialog = Color3.fromRGB(18, 9, 2), DialogHolder = Color3.fromRGB(12, 6, 1),
        DialogHolderLine = Color3.fromRGB(185, 120, 25), DialogButton = Color3.fromRGB(22, 11, 3),
        DialogButtonBorder = Color3.fromRGB(190, 125, 25), DialogBorder = Color3.fromRGB(140, 88, 18),
        DialogInput = Color3.fromRGB(32, 16, 4), DialogInputLine = Color3.fromRGB(255, 195, 80),
        Text = Color3.fromRGB(255, 245, 225), SubText = Color3.fromRGB(230, 195, 145),
        Hover = Color3.fromRGB(255, 170, 40), HoverChange = 0.05, ShineEnabled = true,
        Shine = { Speed = 0.6, RotationSpeed = 25, ColorSequence = ColorSequence.new({ ColorSequenceKeypoint.new(0, Color3.fromRGB(50, 22, 4)), ColorSequenceKeypoint.new(0.5, Color3.fromRGB(255, 170, 40)), ColorSequenceKeypoint.new(1, Color3.fromRGB(50, 22, 4)) }) },
        StrokeShine = true, StrokeDark = Color3.fromRGB(185, 120, 25),
        Background = "rbxassetid://107795771598485", BackgroundTransparency = 0.12,
        ThemeAccentColors = { Color3.fromRGB(255, 170, 40) },
    },
    ["Deep Violet"] = {
        Name = "Deep Violet", Accent = Color3.fromRGB(97, 62, 167),
        AcrylicMain = Color3.fromRGB(20, 20, 20), AcrylicBorder = Color3.fromRGB(110, 90, 130),
        AcrylicGradient = ColorSequence.new(Color3.fromRGB(85, 57, 139), Color3.fromRGB(40, 25, 65)),
        AcrylicNoise = 0.92, TitleBarLine = Color3.fromRGB(95, 75, 110),
        Tab = Color3.fromRGB(160, 140, 180), Element = Color3.fromRGB(140, 120, 160),
        ElementBorder = Color3.fromRGB(60, 50, 70), InElementBorder = Color3.fromRGB(100, 90, 110),
        ElementTransparency = 0.87, ToggleSlider = Color3.fromRGB(140, 120, 160),
        ToggleToggled = Color3.fromRGB(0, 0, 0), SliderRail = Color3.fromRGB(140, 120, 160),
        DropdownFrame = Color3.fromRGB(170, 160, 200), DropdownHolder = Color3.fromRGB(60, 45, 80),
        DropdownBorder = Color3.fromRGB(50, 40, 65), DropdownOption = Color3.fromRGB(140, 120, 160),
        Keybind = Color3.fromRGB(140, 120, 160), Input = Color3.fromRGB(140, 120, 160),
        InputFocused = Color3.fromRGB(20, 10, 30), InputIndicator = Color3.fromRGB(170, 150, 190),
        Dialog = Color3.fromRGB(60, 45, 80), DialogHolder = Color3.fromRGB(45, 30, 65),
        DialogHolderLine = Color3.fromRGB(40, 25, 60), DialogButton = Color3.fromRGB(60, 45, 80),
        DialogButtonBorder = Color3.fromRGB(95, 80, 110), DialogBorder = Color3.fromRGB(85, 70, 100),
        DialogInput = Color3.fromRGB(70, 55, 85), DialogInputLine = Color3.fromRGB(175, 160, 190),
        Text = Color3.fromRGB(240, 240, 240), SubText = Color3.fromRGB(170, 170, 170),
        Hover = Color3.fromRGB(140, 120, 160), HoverChange = 0.04, ShineEnabled = true,
        Shine = { Speed = 0.5, RotationSpeed = 25, ColorSequence = ColorSequence.new({ ColorSequenceKeypoint.new(0, Color3.fromRGB(40, 25, 65)), ColorSequenceKeypoint.new(0.5, Color3.fromRGB(160, 120, 220)), ColorSequenceKeypoint.new(1, Color3.fromRGB(40, 25, 65)) }) },
        StrokeShine = true, StrokeDark = Color3.fromRGB(110, 90, 130),
        Background = "rbxassetid://136310484943077", BackgroundTransparency = 0.15,
        ThemeAccentColors = { Color3.fromRGB(97, 62, 167) },
    },
    ["Neon Purple"] = {
        Name = "Neon Purple", Accent = Color3.fromRGB(180, 0, 255),
        AcrylicMain = Color3.fromRGB(5, 0, 15), AcrylicBorder = Color3.fromRGB(140, 0, 255),
        AcrylicGradient = ColorSequence.new(Color3.fromRGB(5, 0, 15), Color3.fromRGB(45, 0, 160)),
        AcrylicNoise = 0.9, TitleBarLine = Color3.fromRGB(160, 0, 255),
        Tab = Color3.fromRGB(130, 0, 230), Element = Color3.fromRGB(120, 0, 210),
        ElementBorder = Color3.fromRGB(50, 0, 100), InElementBorder = Color3.fromRGB(155, 0, 245),
        ElementTransparency = 0.87, ToggleSlider = Color3.fromRGB(180, 0, 255),
        ToggleToggled = Color3.fromRGB(15, 0, 40), SliderRail = Color3.fromRGB(130, 0, 230),
        DropdownFrame = Color3.fromRGB(255, 255, 255), DropdownHolder = Color3.fromRGB(10, 0, 30),
        DropdownBorder = Color3.fromRGB(50, 0, 140), DropdownOption = Color3.fromRGB(180, 0, 255),
        Keybind = Color3.fromRGB(120, 0, 210), Input = Color3.fromRGB(255, 255, 255),
        InputFocused = Color3.fromRGB(20, 0, 50), InputIndicator = Color3.fromRGB(200, 0, 255),
        Dialog = Color3.fromRGB(10, 0, 30), DialogHolder = Color3.fromRGB(5, 0, 20),
        DialogHolderLine = Color3.fromRGB(3, 0, 12), DialogButton = Color3.fromRGB(10, 0, 30),
        DialogButtonBorder = Color3.fromRGB(140, 0, 255), DialogBorder = Color3.fromRGB(50, 0, 120),
        DialogInput = Color3.fromRGB(25, 0, 60), DialogInputLine = Color3.fromRGB(200, 0, 255),
        Text = Color3.fromRGB(252, 245, 255), SubText = Color3.fromRGB(210, 185, 255),
        Hover = Color3.fromRGB(150, 0, 255), HoverChange = 0.07, ShineEnabled = true,
        Shine = { Speed = 0.4, RotationSpeed = 20, ColorSequence = ColorSequence.new({ ColorSequenceKeypoint.new(0, Color3.fromRGB(32, 5, 137)), ColorSequenceKeypoint.new(0.5, Color3.fromRGB(171, 32, 253)), ColorSequenceKeypoint.new(1, Color3.fromRGB(32, 5, 137)) }) },
        StrokeShine = true, StrokeDark = Color3.fromRGB(60, 0, 150),
        ThemeAccentColors = { Color3.fromRGB(180, 0, 255) },
    },
    ["Royal Blue"] = {
        Name = "Royal Blue", Accent = Color3.fromRGB(15, 82, 186),
        AcrylicMain = Color3.fromRGB(10, 25, 50), AcrylicBorder = Color3.fromRGB(10, 65, 150),
        AcrylicGradient = ColorSequence.new(Color3.fromRGB(12, 70, 160), Color3.fromRGB(8, 20, 45)),
        AcrylicNoise = 0.9, TitleBarLine = Color3.fromRGB(13, 75, 170),
        Tab = Color3.fromRGB(10, 65, 150), Element = Color3.fromRGB(9, 58, 135),
        ElementBorder = Color3.fromRGB(6, 40, 95), InElementBorder = Color3.fromRGB(11, 70, 160),
        ElementTransparency = 0.87, ToggleSlider = Color3.fromRGB(15, 82, 186),
        ToggleToggled = Color3.fromRGB(255, 255, 255), SliderRail = Color3.fromRGB(10, 65, 150),
        DropdownFrame = Color3.fromRGB(8, 50, 120), DropdownHolder = Color3.fromRGB(8, 20, 45),
        DropdownBorder = Color3.fromRGB(6, 40, 95), DropdownOption = Color3.fromRGB(15, 82, 186),
        Keybind = Color3.fromRGB(9, 58, 135), Input = Color3.fromRGB(8, 50, 120),
        InputFocused = Color3.fromRGB(5, 15, 35), InputIndicator = Color3.fromRGB(50, 120, 230),
        Dialog = Color3.fromRGB(8, 20, 45), DialogHolder = Color3.fromRGB(5, 15, 35),
        DialogHolderLine = Color3.fromRGB(3, 10, 25), DialogButton = Color3.fromRGB(8, 20, 45),
        DialogButtonBorder = Color3.fromRGB(10, 65, 150), DialogBorder = Color3.fromRGB(6, 40, 95),
        DialogInput = Color3.fromRGB(12, 30, 65), DialogInputLine = Color3.fromRGB(50, 120, 230),
        Text = Color3.fromRGB(220, 235, 255), SubText = Color3.fromRGB(170, 190, 220),
        Hover = Color3.fromRGB(15, 82, 186), HoverChange = 0.05, ShineEnabled = true,
        Shine = { Speed = 0.5, RotationSpeed = 25, ColorSequence = ColorSequence.new({ ColorSequenceKeypoint.new(0, Color3.fromRGB(20, 40, 85)), ColorSequenceKeypoint.new(0.5, Color3.fromRGB(50, 120, 230)), ColorSequenceKeypoint.new(1, Color3.fromRGB(20, 40, 85)) }) },
        StrokeShine = true, StrokeDark = Color3.fromRGB(10, 65, 150),
        ThemeAccentColors = { Color3.fromRGB(15, 82, 186) },
    },
    ["Deep Ocean"] = {
        Name = "Deep Ocean", Accent = Color3.fromRGB(0, 150, 200),
        AcrylicMain = Color3.fromRGB(15, 30, 45), AcrylicBorder = Color3.fromRGB(0, 100, 150),
        AcrylicGradient = ColorSequence.new(Color3.fromRGB(0, 80, 120), Color3.fromRGB(10, 25, 40)),
        AcrylicNoise = 0.9, TitleBarLine = Color3.fromRGB(0, 120, 180),
        Tab = Color3.fromRGB(0, 100, 150), Element = Color3.fromRGB(0, 90, 135),
        ElementBorder = Color3.fromRGB(0, 70, 105), InElementBorder = Color3.fromRGB(0, 110, 165),
        ElementTransparency = 0.87, ToggleSlider = Color3.fromRGB(0, 150, 200),
        ToggleToggled = Color3.fromRGB(255, 255, 255), SliderRail = Color3.fromRGB(0, 100, 150),
        DropdownFrame = Color3.fromRGB(0, 80, 120), DropdownHolder = Color3.fromRGB(10, 25, 40),
        DropdownBorder = Color3.fromRGB(0, 70, 105), DropdownOption = Color3.fromRGB(0, 150, 200),
        Keybind = Color3.fromRGB(0, 90, 135), Input = Color3.fromRGB(0, 80, 120),
        InputFocused = Color3.fromRGB(5, 20, 35), InputIndicator = Color3.fromRGB(0, 200, 255),
        Dialog = Color3.fromRGB(10, 25, 40), DialogHolder = Color3.fromRGB(5, 15, 25),
        DialogHolderLine = Color3.fromRGB(0, 10, 20), DialogButton = Color3.fromRGB(10, 25, 40),
        DialogButtonBorder = Color3.fromRGB(0, 100, 150), DialogBorder = Color3.fromRGB(0, 70, 105),
        DialogInput = Color3.fromRGB(15, 35, 55), DialogInputLine = Color3.fromRGB(0, 200, 255),
        Text = Color3.fromRGB(240, 248, 255), SubText = Color3.fromRGB(180, 210, 230),
        Hover = Color3.fromRGB(0, 150, 200), HoverChange = 0.05, ShineEnabled = true,
        Shine = { Speed = 0.5, RotationSpeed = 25, ColorSequence = ColorSequence.new({ ColorSequenceKeypoint.new(0, Color3.fromRGB(0, 60, 90)), ColorSequenceKeypoint.new(0.5, Color3.fromRGB(0, 200, 255)), ColorSequenceKeypoint.new(1, Color3.fromRGB(0, 60, 90)) }) },
        StrokeShine = true, StrokeDark = Color3.fromRGB(0, 100, 150),
        ThemeAccentColors = { Color3.fromRGB(0, 150, 200) },
    },
    ["Orange"] = {
        Name = "Orange", Accent = Color3.fromRGB(255, 140, 30),
        AcrylicMain = Color3.fromRGB(4, 4, 4), AcrylicBorder = Color3.fromRGB(200, 90, 10),
        AcrylicGradient = ColorSequence.new({ ColorSequenceKeypoint.new(0, Color3.fromRGB(30, 10, 0)), ColorSequenceKeypoint.new(0.5, Color3.fromRGB(10, 5, 0)), ColorSequenceKeypoint.new(1, Color3.fromRGB(0, 0, 0)) }),
        AcrylicNoise = 0.98, TitleBarLine = Color3.fromRGB(180, 75, 5),
        Tab = Color3.fromRGB(180, 80, 10), Element = Color3.fromRGB(22, 10, 2),
        ElementBorder = Color3.fromRGB(45, 20, 5), InElementBorder = Color3.fromRGB(200, 90, 10),
        ElementTransparency = 0.92, ToggleSlider = Color3.fromRGB(255, 140, 30),
        ToggleToggled = Color3.fromRGB(0, 0, 0), SliderRail = Color3.fromRGB(180, 80, 10),
        DropdownFrame = Color3.fromRGB(160, 70, 8), DropdownHolder = Color3.fromRGB(4, 2, 0),
        DropdownBorder = Color3.fromRGB(200, 90, 10), DropdownOption = Color3.fromRGB(255, 140, 30),
        Keybind = Color3.fromRGB(22, 10, 2), Input = Color3.fromRGB(18, 8, 2),
        InputFocused = Color3.fromRGB(2, 1, 0), InputIndicator = Color3.fromRGB(255, 160, 60),
        Dialog = Color3.fromRGB(6, 3, 0), DialogHolder = Color3.fromRGB(4, 2, 0),
        DialogHolderLine = Color3.fromRGB(180, 75, 5), DialogButton = Color3.fromRGB(8, 4, 0),
        DialogButtonBorder = Color3.fromRGB(180, 80, 10), DialogBorder = Color3.fromRGB(120, 50, 5),
        DialogInput = Color3.fromRGB(18, 8, 2), DialogInputLine = Color3.fromRGB(255, 160, 60),
        Text = Color3.fromRGB(255, 240, 220), SubText = Color3.fromRGB(220, 175, 130),
        Hover = Color3.fromRGB(255, 140, 30), HoverChange = 0.05, ShineEnabled = true,
        Shine = { Speed = 0.7, RotationSpeed = 30, ColorSequence = ColorSequence.new({ ColorSequenceKeypoint.new(0, Color3.fromRGB(30, 10, 0)), ColorSequenceKeypoint.new(0.5, Color3.fromRGB(255, 140, 30)), ColorSequenceKeypoint.new(1, Color3.fromRGB(30, 10, 0)) }) },
        StrokeShine = true, StrokeDark = Color3.fromRGB(180, 80, 10),
        Background = "rbxassetid://122033436660262", BackgroundTransparency = 0.05,
        ThemeAccentColors = { Color3.fromRGB(255, 140, 30) },
    },
    ["Charcoal"] = {
        Name = "Charcoal", Accent = Color3.fromRGB(102, 102, 102),
        AcrylicMain = Color3.fromRGB(20, 20, 20), AcrylicBorder = Color3.fromRGB(60, 60, 60),
        AcrylicGradient = ColorSequence.new(Color3.fromRGB(30, 30, 30), Color3.fromRGB(10, 10, 10)),
        AcrylicNoise = 0.9, TitleBarLine = Color3.fromRGB(70, 70, 70),
        Tab = Color3.fromRGB(40, 40, 40), Element = Color3.fromRGB(35, 35, 35),
        ElementBorder = Color3.fromRGB(20, 20, 20), InElementBorder = Color3.fromRGB(45, 45, 45),
        ElementTransparency = 0.9, ToggleSlider = Color3.fromRGB(90, 160, 255),
        ToggleToggled = Color3.fromRGB(0, 0, 0), SliderRail = Color3.fromRGB(60, 60, 60),
        DropdownFrame = Color3.fromRGB(30, 30, 30), DropdownHolder = Color3.fromRGB(20, 20, 20),
        DropdownBorder = Color3.fromRGB(60, 60, 60), DropdownOption = Color3.fromRGB(90, 160, 255),
        Keybind = Color3.fromRGB(35, 35, 35), Input = Color3.fromRGB(25, 25, 25),
        InputFocused = Color3.fromRGB(15, 15, 15), InputIndicator = Color3.fromRGB(120, 180, 255),
        Dialog = Color3.fromRGB(25, 25, 25), DialogHolder = Color3.fromRGB(20, 20, 20),
        DialogHolderLine = Color3.fromRGB(15, 15, 15), DialogButton = Color3.fromRGB(25, 25, 25),
        DialogButtonBorder = Color3.fromRGB(60, 60, 60), DialogBorder = Color3.fromRGB(60, 60, 60),
        DialogInput = Color3.fromRGB(30, 30, 30), DialogInputLine = Color3.fromRGB(120, 180, 255),
        Text = Color3.fromRGB(240, 240, 240), SubText = Color3.fromRGB(170, 170, 170),
        Hover = Color3.fromRGB(90, 160, 255), HoverChange = 0.05, ShineEnabled = false,
        StrokeShine = false, StrokeDark = Color3.fromRGB(60, 60, 60),
        ThemeAccentColors = { Color3.fromRGB(102, 102, 102) },
    },
    ["Pearl White"] = {
        Name = "Pearl White", Accent = Color3.fromRGB(214, 214, 214),
        AcrylicMain = Color3.fromRGB(240, 240, 240), AcrylicBorder = Color3.fromRGB(200, 200, 200),
        AcrylicGradient = ColorSequence.new(Color3.fromRGB(255, 255, 255), Color3.fromRGB(220, 220, 220)),
        AcrylicNoise = 0.9, TitleBarLine = Color3.fromRGB(200, 200, 200),
        Tab = Color3.fromRGB(230, 230, 230), Element = Color3.fromRGB(255, 255, 255),
        ElementBorder = Color3.fromRGB(210, 210, 210), InElementBorder = Color3.fromRGB(210, 210, 210),
        ElementTransparency = 0.85, ToggleSlider = Color3.fromRGB(60, 160, 255),
        ToggleToggled = Color3.fromRGB(255, 255, 255), SliderRail = Color3.fromRGB(200, 200, 200),
        DropdownFrame = Color3.fromRGB(230, 230, 230), DropdownHolder = Color3.fromRGB(220, 220, 220),
        DropdownBorder = Color3.fromRGB(200, 200, 200), DropdownOption = Color3.fromRGB(60, 160, 255),
        Keybind = Color3.fromRGB(220, 220, 220), Input = Color3.fromRGB(230, 230, 230),
        InputFocused = Color3.fromRGB(210, 210, 210), InputIndicator = Color3.fromRGB(60, 160, 255),
        Dialog = Color3.fromRGB(230, 230, 230), DialogHolder = Color3.fromRGB(220, 220, 220),
        DialogHolderLine = Color3.fromRGB(210, 210, 210), DialogButton = Color3.fromRGB(230, 230, 230),
        DialogButtonBorder = Color3.fromRGB(200, 200, 200), DialogBorder = Color3.fromRGB(200, 200, 200),
        DialogInput = Color3.fromRGB(240, 240, 240), DialogInputLine = Color3.fromRGB(60, 160, 255),
        Text = Color3.fromRGB(20, 20, 20), SubText = Color3.fromRGB(90, 90, 90),
        Hover = Color3.fromRGB(60, 160, 255), HoverChange = 0.05, ShineEnabled = false,
        StrokeShine = false, StrokeDark = Color3.fromRGB(200, 200, 200),
        ThemeAccentColors = { Color3.fromRGB(214, 214, 214) },
    },
    ["Midnight Blue"] = {
        Name = "Midnight Blue", Accent = Color3.fromRGB(100, 80, 200),
        AcrylicMain = Color3.fromRGB(10, 8, 25), AcrylicBorder = Color3.fromRGB(60, 45, 140),
        AcrylicGradient = ColorSequence.new(Color3.fromRGB(50, 35, 120), Color3.fromRGB(8, 5, 20)),
        AcrylicNoise = 0.9, TitleBarLine = Color3.fromRGB(80, 60, 170),
        Tab = Color3.fromRGB(60, 45, 140), Element = Color3.fromRGB(55, 40, 125),
        ElementBorder = Color3.fromRGB(30, 20, 70), InElementBorder = Color3.fromRGB(70, 55, 155),
        ElementTransparency = 0.87, ToggleSlider = Color3.fromRGB(100, 80, 200),
        ToggleToggled = Color3.fromRGB(255, 255, 255), SliderRail = Color3.fromRGB(60, 45, 140),
        DropdownFrame = Color3.fromRGB(45, 30, 110), DropdownHolder = Color3.fromRGB(8, 5, 20),
        DropdownBorder = Color3.fromRGB(35, 25, 85), DropdownOption = Color3.fromRGB(100, 80, 200),
        Keybind = Color3.fromRGB(55, 40, 125), Input = Color3.fromRGB(45, 30, 110),
        InputFocused = Color3.fromRGB(5, 3, 15), InputIndicator = Color3.fromRGB(140, 120, 240),
        Dialog = Color3.fromRGB(8, 5, 20), DialogHolder = Color3.fromRGB(5, 3, 15),
        DialogHolderLine = Color3.fromRGB(3, 2, 10), DialogButton = Color3.fromRGB(8, 5, 20),
        DialogButtonBorder = Color3.fromRGB(60, 45, 140), DialogBorder = Color3.fromRGB(40, 30, 90),
        DialogInput = Color3.fromRGB(15, 10, 35), DialogInputLine = Color3.fromRGB(140, 120, 240),
        Text = Color3.fromRGB(220, 220, 255), SubText = Color3.fromRGB(170, 170, 210),
        Hover = Color3.fromRGB(100, 80, 200), HoverChange = 0.05, ShineEnabled = true,
        Shine = { Speed = 0.5, RotationSpeed = 25, ColorSequence = ColorSequence.new({ ColorSequenceKeypoint.new(0, Color3.fromRGB(25, 15, 60)), ColorSequenceKeypoint.new(0.5, Color3.fromRGB(140, 120, 240)), ColorSequenceKeypoint.new(1, Color3.fromRGB(25, 15, 60)) }) },
        StrokeShine = true, StrokeDark = Color3.fromRGB(60, 45, 140),
        ThemeAccentColors = { Color3.fromRGB(100, 80, 200) },
    },
    ["Galaxy Purple"] = {
        Name = "Galaxy Purple", Accent = Color3.fromRGB(160, 60, 220),
        AcrylicMain = Color3.fromRGB(12, 5, 25), AcrylicBorder = Color3.fromRGB(120, 40, 185),
        AcrylicGradient = ColorSequence.new(Color3.fromRGB(110, 35, 175), Color3.fromRGB(8, 3, 20)),
        AcrylicNoise = 0.9, TitleBarLine = Color3.fromRGB(130, 50, 195),
        Tab = Color3.fromRGB(125, 45, 190), Element = Color3.fromRGB(112, 40, 170),
        ElementBorder = Color3.fromRGB(50, 18, 80), InElementBorder = Color3.fromRGB(130, 50, 195),
        ElementTransparency = 0.87, ToggleSlider = Color3.fromRGB(160, 60, 220),
        ToggleToggled = Color3.fromRGB(255, 255, 255), SliderRail = Color3.fromRGB(125, 45, 190),
        DropdownFrame = Color3.fromRGB(100, 35, 152), DropdownHolder = Color3.fromRGB(8, 3, 20),
        DropdownBorder = Color3.fromRGB(72, 24, 108), DropdownOption = Color3.fromRGB(160, 60, 220),
        Keybind = Color3.fromRGB(112, 40, 170), Input = Color3.fromRGB(100, 35, 152),
        InputFocused = Color3.fromRGB(5, 2, 14), InputIndicator = Color3.fromRGB(195, 100, 255),
        Dialog = Color3.fromRGB(8, 3, 20), DialogHolder = Color3.fromRGB(5, 2, 14),
        DialogHolderLine = Color3.fromRGB(3, 1, 9), DialogButton = Color3.fromRGB(8, 3, 20),
        DialogButtonBorder = Color3.fromRGB(125, 45, 190), DialogBorder = Color3.fromRGB(75, 25, 115),
        DialogInput = Color3.fromRGB(22, 10, 50), DialogInputLine = Color3.fromRGB(195, 100, 255),
        Text = Color3.fromRGB(242, 232, 255), SubText = Color3.fromRGB(200, 178, 228),
        Hover = Color3.fromRGB(160, 60, 220), HoverChange = 0.05, ShineEnabled = true,
        Shine = { Speed = 0.5, RotationSpeed = 25, ColorSequence = ColorSequence.new({ ColorSequenceKeypoint.new(0, Color3.fromRGB(48, 18, 85)), ColorSequenceKeypoint.new(0.5, Color3.fromRGB(195, 100, 255)), ColorSequenceKeypoint.new(1, Color3.fromRGB(48, 18, 85)) }) },
        StrokeShine = true, StrokeDark = Color3.fromRGB(125, 45, 190),
        ThemeAccentColors = { Color3.fromRGB(160, 60, 220) },
    },
    ["Cosmic Violet"] = {
        Name = "Cosmic Violet", Accent = Color3.fromRGB(80, 60, 140),
        AcrylicMain = Color3.fromRGB(12, 10, 22), AcrylicBorder = Color3.fromRGB(50, 35, 110),
        AcrylicGradient = ColorSequence.new(Color3.fromRGB(45, 30, 100), Color3.fromRGB(8, 6, 16)),
        AcrylicNoise = 0.9, TitleBarLine = Color3.fromRGB(60, 42, 120),
        Tab = Color3.fromRGB(55, 38, 115), Element = Color3.fromRGB(50, 34, 104),
        ElementBorder = Color3.fromRGB(25, 18, 55), InElementBorder = Color3.fromRGB(60, 42, 120),
        ElementTransparency = 0.87, ToggleSlider = Color3.fromRGB(80, 60, 140),
        ToggleToggled = Color3.fromRGB(255, 255, 255), SliderRail = Color3.fromRGB(55, 38, 115),
        DropdownFrame = Color3.fromRGB(44, 30, 92), DropdownHolder = Color3.fromRGB(8, 6, 16),
        DropdownBorder = Color3.fromRGB(32, 22, 68), DropdownOption = Color3.fromRGB(80, 60, 140),
        Keybind = Color3.fromRGB(50, 34, 104), Input = Color3.fromRGB(44, 30, 92),
        InputFocused = Color3.fromRGB(5, 3, 10), InputIndicator = Color3.fromRGB(115, 90, 175),
        Dialog = Color3.fromRGB(8, 6, 16), DialogHolder = Color3.fromRGB(5, 3, 10),
        DialogHolderLine = Color3.fromRGB(3, 2, 6), DialogButton = Color3.fromRGB(8, 6, 16),
        DialogButtonBorder = Color3.fromRGB(55, 38, 115), DialogBorder = Color3.fromRGB(34, 23, 70),
        DialogInput = Color3.fromRGB(22, 16, 45), DialogInputLine = Color3.fromRGB(115, 90, 175),
        Text = Color3.fromRGB(230, 225, 245), SubText = Color3.fromRGB(185, 175, 210),
        Hover = Color3.fromRGB(80, 60, 140), HoverChange = 0.05, ShineEnabled = true,
        Shine = { Speed = 0.5, RotationSpeed = 25, ColorSequence = ColorSequence.new({ ColorSequenceKeypoint.new(0, Color3.fromRGB(35, 25, 65)), ColorSequenceKeypoint.new(0.5, Color3.fromRGB(115, 90, 175)), ColorSequenceKeypoint.new(1, Color3.fromRGB(35, 25, 65)) }) },
        StrokeShine = true, StrokeDark = Color3.fromRGB(55, 38, 115),
        ThemeAccentColors = { Color3.fromRGB(80, 60, 140) },
    },
    ["Cotton Candy"] = {
        Name = "Cotton Candy", Accent = Color3.fromRGB(255, 130, 190),
        AcrylicMain = Color3.fromRGB(255, 225, 245), AcrylicBorder = Color3.fromRGB(255, 190, 230),
        AcrylicGradient = ColorSequence.new(Color3.fromRGB(255, 235, 250), Color3.fromRGB(235, 210, 255)),
        AcrylicNoise = 0.96, TitleBarLine = Color3.fromRGB(240, 180, 225),
        Tab = Color3.fromRGB(195, 130, 185), Element = Color3.fromRGB(255, 200, 235),
        ElementBorder = Color3.fromRGB(230, 165, 210), InElementBorder = Color3.fromRGB(235, 170, 215),
        ElementTransparency = 0.70, ToggleSlider = Color3.fromRGB(215, 145, 192),
        ToggleToggled = Color3.fromRGB(90, 30, 70), SliderRail = Color3.fromRGB(235, 170, 215),
        DropdownFrame = Color3.fromRGB(248, 192, 230), DropdownHolder = Color3.fromRGB(255, 225, 248),
        DropdownBorder = Color3.fromRGB(228, 168, 213), DropdownOption = Color3.fromRGB(205, 140, 188),
        Keybind = Color3.fromRGB(228, 168, 213), Input = Color3.fromRGB(250, 210, 238),
        InputFocused = Color3.fromRGB(195, 125, 168), InputIndicator = Color3.fromRGB(250, 195, 232),
        Dialog = Color3.fromRGB(255, 228, 248), DialogHolder = Color3.fromRGB(255, 238, 252),
        DialogHolderLine = Color3.fromRGB(238, 208, 235), DialogButton = Color3.fromRGB(255, 233, 250),
        DialogButtonBorder = Color3.fromRGB(228, 178, 218), DialogBorder = Color3.fromRGB(238, 188, 226),
        DialogInput = Color3.fromRGB(250, 213, 240), DialogInputLine = Color3.fromRGB(228, 172, 215),
        Text = Color3.fromRGB(75, 25, 55), SubText = Color3.fromRGB(145, 75, 115),
        Hover = Color3.fromRGB(238, 182, 222), HoverChange = 0.04, ShineEnabled = true,
        Shine = { Speed = 0.4, RotationSpeed = 18, ColorSequence = ColorSequence.new({ ColorSequenceKeypoint.new(0, Color3.fromRGB(255, 180, 220)), ColorSequenceKeypoint.new(0.5, Color3.fromRGB(220, 180, 255)), ColorSequenceKeypoint.new(1, Color3.fromRGB(255, 180, 220)) }) },
        StrokeShine = true, StrokeDark = Color3.fromRGB(228, 172, 213),
        ThemeAccentColors = { Color3.fromRGB(255, 130, 190) },
    },
    ["Arctic Frost"] = {
        Name = "Arctic Frost", Accent = Color3.fromRGB(100, 180, 240),
        AcrylicMain = Color3.fromRGB(185, 215, 235), AcrylicBorder = Color3.fromRGB(200, 228, 248),
        AcrylicGradient = ColorSequence.new(Color3.fromRGB(235, 248, 255), Color3.fromRGB(210, 235, 250)),
        AcrylicNoise = 0.97, TitleBarLine = Color3.fromRGB(180, 215, 240),
        Tab = Color3.fromRGB(90, 150, 200), Element = Color3.fromRGB(210, 235, 250),
        ElementBorder = Color3.fromRGB(170, 200, 225), InElementBorder = Color3.fromRGB(140, 185, 218),
        ElementTransparency = 0.65, ToggleSlider = Color3.fromRGB(120, 175, 215),
        ToggleToggled = Color3.fromRGB(30, 70, 120), SliderRail = Color3.fromRGB(150, 200, 235),
        DropdownFrame = Color3.fromRGB(190, 225, 248), DropdownHolder = Color3.fromRGB(225, 242, 255),
        DropdownBorder = Color3.fromRGB(170, 210, 238), DropdownOption = Color3.fromRGB(130, 180, 220),
        Keybind = Color3.fromRGB(150, 200, 235), Input = Color3.fromRGB(200, 230, 248),
        InputFocused = Color3.fromRGB(100, 150, 190), InputIndicator = Color3.fromRGB(160, 210, 240),
        Dialog = Color3.fromRGB(220, 240, 255), DialogHolder = Color3.fromRGB(235, 248, 255),
        DialogHolderLine = Color3.fromRGB(200, 228, 248), DialogButton = Color3.fromRGB(225, 242, 255),
        DialogButtonBorder = Color3.fromRGB(170, 210, 238), DialogBorder = Color3.fromRGB(180, 215, 240),
        DialogInput = Color3.fromRGB(200, 230, 248), DialogInputLine = Color3.fromRGB(150, 200, 235),
        Text = Color3.fromRGB(20, 40, 70), SubText = Color3.fromRGB(65, 105, 148),
        Hover = Color3.fromRGB(170, 210, 238), HoverChange = 0.04, ShineEnabled = true,
        Shine = { Speed = 0.3, RotationSpeed = 15, ColorSequence = ColorSequence.new({ ColorSequenceKeypoint.new(0, Color3.fromRGB(200, 235, 255)), ColorSequenceKeypoint.new(0.5, Color3.fromRGB(255, 255, 255)), ColorSequenceKeypoint.new(1, Color3.fromRGB(200, 235, 255)) }) },
        StrokeShine = true, StrokeDark = Color3.fromRGB(170, 210, 238),
        ThemeAccentColors = { Color3.fromRGB(100, 180, 240) },
    }
}

WindUI.Themes = Themes
WindUI.ThemeNames = {}
for name, _ in pairs(Themes) do
    table.insert(WindUI.ThemeNames, name)
end
table.sort(WindUI.ThemeNames)

-- Animation & RGB Engine
local Animation = {}
local _animConns = {}
local _rgbConn = nil

function Animation.Apply(themeName, root)
    for _, c in ipairs(_animConns) do pcall(function() c:Disconnect() end) end
    table.clear(_animConns)
    local theme = WindUI.Themes[themeName]
    if not theme or not root or not WindUI.ShineEnabled or not theme.ShineEnabled or not theme.Shine then return end
    local ShineConfig = theme.Shine
    local Speed = ShineConfig.Speed or 0.5
    local RotationSpeed = ShineConfig.RotationSpeed or 25
    local ColorSeq = ShineConfig.ColorSequence
    for _, obj in ipairs(root:GetDescendants()) do
        if obj:IsA("UIGradient") and obj.Name == "_ShineGradient" then
            local conn = Services.RunService.RenderStepped:Connect(function(dt)
                local t = (obj:GetAttribute("_t") or 0) + dt * Speed
                obj:SetAttribute("_t", t)
                obj.Rotation = (t * RotationSpeed) % 360
                if ColorSeq then obj.Color = ColorSeq end
            end)
            table.insert(_animConns, conn)
        end
        if obj:IsA("UIStroke") and theme.StrokeShine and obj.Name == "_ShineStroke" then
            local from = theme.StrokeDark or theme.InElementBorder
            local shine = theme.Accent
            local conn = Services.RunService.RenderStepped:Connect(function(dt)
                local t = (obj:GetAttribute("_t") or 0) + dt * Speed
                obj:SetAttribute("_t", t)
                obj.Color = from:Lerp(shine, (math.sin(t * 3) + 1) / 2)
            end)
            table.insert(_animConns, conn)
        end
    end
end

function WindUI.StartRGBMode()
    if _rgbConn then _rgbConn:Disconnect(); _rgbConn = nil end
    local hue = 0
    _rgbConn = Services.RunService.RenderStepped:Connect(function(dt)
        if WindUI.Theme ~= "RGB" then _rgbConn:Disconnect(); _rgbConn = nil; return end
        hue = (hue + dt * 0.12) % 1
        local col = Color3.fromHSV(hue, 1, 1)
        local thm = WindUI.Themes["RGB"]
        if thm then
            thm.Accent = col; thm.AcrylicBorder = col; thm.InElementBorder = col
            thm.DropdownBorder = col; thm.DropdownFrame = col; thm.DropdownOption = col
            thm.Tab = col; thm.TitleBarLine = col
            Creator.UpdateTheme()
        end
    end)
end

function WindUI.StopRGBMode()
    if _rgbConn then _rgbConn:Disconnect(); _rgbConn = nil end
end

function WindUI:SetTheme(themeName)
    if not WindUI.Themes[themeName] then return end
    WindUI.StopRGBMode()
    WindUI.Theme = themeName
    Creator.UpdateTheme()
    if themeName == "RGB" then
        WindUI.StartRGBMode()
    end
    if WindUI.Window and WindUI.Window.Root then
        Animation.Apply(themeName, WindUI.Window.Root)
    end
end

function WindUI:RegisterCustomTheme(name, themeData)
    if type(name) ~= "string" or type(themeData) ~= "table" then return false end
    themeData.Name = name
    if not themeData.ThemeAccentColors and themeData.Accent then
        themeData.ThemeAccentColors = { themeData.Accent }
    end
    WindUI.Themes[name] = themeData
    if not table.find(WindUI.ThemeNames, name) then
        table.insert(WindUI.ThemeNames, name)
        table.sort(WindUI.ThemeNames)
    end
    return true
end
WindUI.AddCustomTheme = WindUI.RegisterCustomTheme
""")
print("Part 3 added.")

# PART 4: Icon Engine & Acrylic Glass Blur Engine
code_parts.append("""
--[[
================================================================================
    Icon Engine (GetIcon with CDNs & Built-in Vector Sheets)
================================================================================
--]]
local IconCache = {}
local IconURLs = {
    lucide = "https://raw.githubusercontent.com/StyearX/Icons/refs/heads/main/lucide/dist/Icons.lua",
    gravity = "https://raw.githubusercontent.com/StyearX/Icons/refs/heads/main/gravity/dist/Icons.lua",
    solar = "https://raw.githubusercontent.com/StyearX/Icons/refs/heads/main/solar/dist/Icons.lua",
    sfsymbols = "https://raw.githubusercontent.com/StyearX/Icons/refs/heads/main/sfsymbols/dist/Icons.lua",
    craft = "https://raw.githubusercontent.com/StyearX/Icons/refs/heads/main/craft/dist/Icons.lua",
    hero = "https://raw.githubusercontent.com/StyearX/Icons/refs/heads/main/hero/dist/Icons.lua",
    gmi = "https://raw.githubusercontent.com/StyearX/Icons/refs/heads/main/GoogleMaterialIcons/dist/Icons.lua",
}

local FallbackIcons = {
    ["lucide-home"] = "rbxassetid://10723407389",
    ["lucide-settings"] = "rbxassetid://10734950309",
    ["lucide-user"] = "rbxassetid://10747373176",
    ["lucide-folder"] = "rbxassetid://10723387563",
    ["lucide-file-text"] = "rbxassetid://10723367380",
    ["lucide-check"] = "rbxassetid://10709790644",
    ["lucide-x"] = "rbxassetid://10747384394",
    ["lucide-search"] = "rbxassetid://10734943674",
    ["lucide-trash-2"] = "rbxassetid://10747362241",
    ["lucide-refresh-cw"] = "rbxassetid://10734933222",
    ["lucide-download"] = "rbxassetid://10723344270",
    ["lucide-upload"] = "rbxassetid://10747366434",
    ["lucide-shield"] = "rbxassetid://10734951847",
    ["lucide-key"] = "rbxassetid://10723416652",
    ["lucide-lock"] = "rbxassetid://10723434711",
    ["lucide-unlock"] = "rbxassetid://10747366027",
    ["lucide-star"] = "rbxassetid://10734966248",
    ["lucide-code"] = "rbxassetid://10709810463",
    ["lucide-terminal"] = "rbxassetid://10734982144",
    ["lucide-eye"] = "rbxassetid://10723346959",
    ["lucide-eye-off"] = "rbxassetid://10723346871",
    ["lucide-chevron-down"] = "rbxassetid://10709790948",
    ["lucide-chevron-up"] = "rbxassetid://10709791523",
    ["lucide-chevron-left"] = "rbxassetid://10709791281",
    ["lucide-chevron-right"] = "rbxassetid://10709791437",
    ["lucide-plus"] = "rbxassetid://10734924532",
    ["lucide-minus"] = "rbxassetid://10734896206",
    ["lucide-menu"] = "rbxassetid://10734887784",
    ["lucide-sliders"] = "rbxassetid://10734963400",
    ["lucide-palette"] = "rbxassetid://10734910430",
    ["lucide-bell"] = "rbxassetid://10709781824",
    ["lucide-bookmark"] = "rbxassetid://10709782154",
    ["lucide-copy"] = "rbxassetid://10709812159",
    ["lucide-edit"] = "rbxassetid://10734883598",
}

local function LoadIconSource(prefix)
    if IconCache[prefix] then return IconCache[prefix] end
    local url = IconURLs[prefix]
    if not url then return nil end
    local ok, result = pcall(function()
        return loadstring(game:HttpGet(url, true))()
    end)
    if not ok then
        return nil
    end
    if result and result.Icons then
        IconCache[prefix] = { _sprites = result.Spritesheets, _icons = result.Icons }
    else
        IconCache[prefix] = result
    end
    return IconCache[prefix]
end

function WindUI:GetIcon(iconSpec)
    if iconSpec == nil or iconSpec == "" then return nil end
    if type(iconSpec) == "table" then return iconSpec end
    if iconSpec:match("^rbxassetid://") or iconSpec:match("^rbxasset://") or tonumber(iconSpec) then
        return { Image = tonumber(iconSpec) and ("rbxassetid://" .. iconSpec) or iconSpec }
    end
    local prefix, name = iconSpec:match("^(.-)%/(.+)$")
    if prefix then
        local src = LoadIconSource(prefix)
        if src then
            if src._icons then
                local entry = src._icons[name]
                if entry then
                    local sheetId = src._sprites[tostring(entry.Image)]
                    return { Image = sheetId, ImageRectOffset = entry.ImageRectPosition, ImageRectSize = entry.ImageRectSize }
                end
            else
                return src[name]
            end
        end
    end
    local lucide = LoadIconSource("lucide")
    if lucide and lucide[iconSpec] then return lucide[iconSpec] end
    if lucide and lucide["lucide-" .. iconSpec] then return lucide["lucide-" .. iconSpec] end
    if FallbackIcons["lucide-" .. iconSpec] then return { Image = FallbackIcons["lucide-" .. iconSpec] } end
    if FallbackIcons[iconSpec] then return { Image = FallbackIcons[iconSpec] } end
    return { Image = "rbxassetid://10723407389" }
end

--[[
================================================================================
    Acrylic Glass Blur & DepthOfField Engine
================================================================================
--]]
local AcrylicEngine = {
    _dof = nil,
    _models = {},
}

function AcrylicEngine.Init()
    if AcrylicEngine._dof then return end
    pcall(function()
        local dof = Instance.new("DepthOfFieldEffect")
        dof.Name = "__WindUIAcrylicBlur"
        dof.FarIntensity = 0
        dof.InFocusRadius = 0.1
        dof.NearIntensity = 1
        dof.Parent = Services.Lighting
        AcrylicEngine._dof = dof
    end)
end

function AcrylicEngine.CreateAcrylic(frame)
    local model = Instance.new("Part")
    model.Name = "__WindUIAcrylicPart"
    model.Color = Color3.new(0, 0, 0)
    model.Material = Enum.Material.Glass
    model.Size = Vector3.new(1, 1, 0)
    model.Anchored = true
    model.CanCollide = false
    model.CanQuery = false
    model.CanTouch = false
    model.Locked = true
    model.CastShadow = false
    model.Transparency = 0.98
    local mesh = Instance.new("SpecialMesh")
    mesh.MeshType = Enum.MeshType.Brick
    mesh.Offset = Vector3.new(0, 0, -1e-6)
    mesh.Parent = model
    model.Parent = Services.Workspace

    local function updatePart()
        if not frame or not frame.Parent or not model or not model.Parent then return end
        local cam = Services.Workspace.CurrentCamera
        if not cam then return end
        local absPos, absSize = frame.AbsolutePosition, frame.AbsoluteSize
        local tl = cam:ScreenPointToRay(absPos.X, absPos.Y).Origin + cam:ScreenPointToRay(absPos.X, absPos.Y).Direction * 0.001
        local tr = cam:ScreenPointToRay(absPos.X + absSize.X, absPos.Y).Origin + cam:ScreenPointToRay(absPos.X + absSize.X, absPos.Y).Direction * 0.001
        local br = cam:ScreenPointToRay(absPos.X + absSize.X, absPos.Y + absSize.Y).Origin + cam:ScreenPointToRay(absPos.X + absSize.X, absPos.Y + absSize.Y).Direction * 0.001
        local w = (tr - tl).Magnitude
        local h = (br - tr).Magnitude
        model.CFrame = CFrame.fromMatrix((tl + br) / 2, cam.CFrame.XVector, cam.CFrame.YVector, cam.CFrame.ZVector)
        mesh.Scale = Vector3.new(w, h, 0)
    end

    local conns = {}
    table.insert(conns, frame:GetPropertyChangedSignal("AbsolutePosition"):Connect(updatePart))
    table.insert(conns, frame:GetPropertyChangedSignal("AbsoluteSize"):Connect(updatePart))
    table.insert(conns, frame:GetPropertyChangedSignal("Visible"):Connect(function()
        model.Transparency = frame.Visible and 0.98 or 1
    end))
    table.insert(conns, Services.RunService.RenderStepped:Connect(updatePart))

    frame.AncestryChanged:Connect(function()
        if not frame.Parent then
            for _, c in ipairs(conns) do pcall(function() c:Disconnect() end) end
            pcall(function() model:Destroy() end)
        end
    end)
    task.defer(updatePart)
    return {
        Model = model,
        SetVisibility = function(vis)
            model.Transparency = vis and 0.98 or 1
        end
    }
end

function AcrylicEngine.AcrylicPaint()
    local container = Creator.New("Frame", {
        Size = UDim2.fromScale(1, 1),
        BackgroundTransparency = 0.9,
        BackgroundColor3 = Color3.fromRGB(255, 255, 255),
        BorderSizePixel = 0
    }, {
        Creator.New("ImageLabel", {
            Image = "rbxassetid://8992230677",
            ScaleType = Enum.ScaleType.Slice,
            SliceCenter = Rect.new(Vector2.new(99, 99), Vector2.new(99, 99)),
            AnchorPoint = Vector2.new(0.5, 0.5),
            Size = UDim2.new(1, 120, 1, 116),
            Position = UDim2.new(0.5, 0, 0.5, 0),
            BackgroundTransparency = 1,
            ImageColor3 = Color3.fromRGB(0, 0, 0),
            ImageTransparency = 0.65
        }),
        Creator.New("UICorner", { CornerRadius = UDim.new(0, 10) }),
        Creator.New("Frame", {
            BackgroundTransparency = 0.35,
            Size = UDim2.fromScale(1, 1),
            Name = "__Background",
            ThemeTag = { BackgroundColor3 = "AcrylicMain" }
        }, { Creator.New("UICorner", { CornerRadius = UDim.new(0, 10) }) }),
        Creator.New("Frame", {
            BackgroundColor3 = Color3.fromRGB(255, 255, 255),
            BackgroundTransparency = 0.4,
            Size = UDim2.fromScale(1, 1)
        }, {
            Creator.New("UICorner", { CornerRadius = UDim.new(0, 10) }),
            Creator.New("UIGradient", { Rotation = 90, ThemeTag = { Color = "AcrylicGradient" } })
        }),
        Creator.New("ImageLabel", {
            Name = "__ThemeBG",
            Image = "rbxassetid://9968344105",
            ImageTransparency = 0.96,
            ScaleType = Enum.ScaleType.Tile,
            TileSize = UDim2.new(0, 128, 0, 128),
            Size = UDim2.fromScale(1, 1),
            BackgroundTransparency = 1
        }, { Creator.New("UICorner", { CornerRadius = UDim.new(0, 10) }) }),
        Creator.New("ImageLabel", {
            Name = "__Noise",
            Image = "rbxassetid://9968344227",
            ImageTransparency = 0.9,
            ScaleType = Enum.ScaleType.Tile,
            TileSize = UDim2.new(0, 128, 0, 128),
            Size = UDim2.fromScale(1, 1),
            BackgroundTransparency = 1,
            ThemeTag = { ImageTransparency = "AcrylicNoise" }
        }, { Creator.New("UICorner", { CornerRadius = UDim.new(0, 10) }) }),
        Creator.New("Frame", { BackgroundTransparency = 1, Size = UDim2.fromScale(1, 1), ZIndex = 2 }, {
            Creator.New("UICorner", { CornerRadius = UDim.new(0, 10) }),
            Creator.New("UIStroke", {
                Name = "_ShineStroke",
                Transparency = 0.45,
                Thickness = 1.2,
                ThemeTag = { Color = "AcrylicBorder" }
            })
        })
    })

    local modelHandle
    if WindUI.UseAcrylic then
        AcrylicEngine.Init()
        modelHandle = AcrylicEngine.CreateAcrylic(container)
    end
    return {
        Frame = container,
        Model = modelHandle and modelHandle.Model or nil,
        SetVisibility = function(selfPaint, vis)
            if modelHandle then modelHandle.SetVisibility(vis) end
        end
    }
end

WindUI.AcrylicEngine = AcrylicEngine
""")
print("Part 4 added.")

# PART 5: Key System Modal & External Verification Engine
code_parts.append("""
--[[
================================================================================
    Key System Modal & Verification Engine
================================================================================
--]]
local KeySystem = {}
KeySystem.__index = KeySystem

function KeySystem.Init(windowInstance, keySettings)
    local ks = setmetatable({}, KeySystem)
    ks.Window = windowInstance
    ks.Settings = keySettings or {}
    ks.Title = ks.Settings.Title or "Security Verification"
    ks.SubTitle = ks.Settings.SubTitle or "Please enter your access key to unlock."
    ks.Note = ks.Settings.Note or "Click 'Get Key' to acquire your access token."
    ks.Key = ks.Settings.Key or "WIND-PRO-2026"
    ks.GetKeyURL = ks.Settings.GetKeyURL or "https://example.com/getkey"
    ks.SaveKey = (ks.Settings.SaveKey ~= false)
    ks.KeyFileName = ks.Settings.KeyFileName or "WindUI_Ultimate_Key.json"
    ks.VerifyCallback = ks.Settings.VerifyCallback
    ks.Verified = false
    return ks
end

function KeySystem:CheckSavedKey()
    if not self.SaveKey then return false end
    local hs = Services.HttpService
    local ok, data = pcall(function()
        if isfile and isfile(self.KeyFileName) then
            return hs:JSONDecode(readfile(self.KeyFileName))
        end
    end)
    if ok and type(data) == "table" and data.key then
        return self:VerifyKey(data.key, true)
    end
    return false
end

function KeySystem:SaveKeyToFile(keyString)
    if not self.SaveKey then return end
    local hs = Services.HttpService
    pcall(function()
        if writefile then
            writefile(self.KeyFileName, hs:JSONEncode({ key = keyString, timestamp = os.time() }))
        end
    end)
end

function KeySystem:VerifyKey(enteredKey, isAutoLoad)
    enteredKey = tostring(enteredKey or ""):gsub("^%s+", ""):gsub("%s+$", "")
    if enteredKey == "" then return false end
    
    local isValid = false
    if type(self.Key) == "table" then
        for _, validKey in ipairs(self.Key) do
            if enteredKey == tostring(validKey) then
                isValid = true
                break
            end
        end
    else
        isValid = (enteredKey == tostring(self.Key))
    end

    if self.VerifyCallback then
        local customCheck = self.VerifyCallback(enteredKey)
        if customCheck == true then isValid = true end
    end

    if isValid then
        self.Verified = true
        self:SaveKeyToFile(enteredKey)
        if self.OnSuccess then self.OnSuccess() end
        return true
    end
    return false
end

function KeySystem:Render(onSuccessCallback)
    self.OnSuccess = onSuccessCallback
    if self:CheckSavedKey() then
        if onSuccessCallback then onSuccessCallback() end
        return
    end

    local gui = WindUI.KeySystemGUI
    if not gui then return end

    local tint = Creator.New("TextButton", {
        Name = "KeySystemTint",
        Text = "",
        Size = UDim2.fromScale(1, 1),
        BackgroundColor3 = Color3.fromRGB(0, 0, 0),
        BackgroundTransparency = 1,
        Parent = gui
    })
    local tintMotor, setTint = Creator.SpringMotor(1, tint, "BackgroundTransparency")
    setTint(0.4)

    local scaleHolder = Creator.New("UIScale", { Scale = 0.85 })
    local scaleMotor, setScale = Creator.SpringMotor(0.85, scaleHolder, "Scale")
    setScale(1)

    local cardPaint = AcrylicEngine.AcrylicPaint()
    local cardRoot = Creator.New("CanvasGroup", {
        Name = "KeySystemCard",
        Size = UDim2.fromOffset(440, 280),
        AnchorPoint = Vector2.new(0.5, 0.5),
        Position = UDim2.fromScale(0.5, 0.5),
        GroupTransparency = 1,
        Parent = tint
    }, {
        Creator.New("UICorner", { CornerRadius = UDim.new(0, 12) }),
        scaleHolder,
        cardPaint.Frame
    })
    local transMotor, setTrans = Creator.SpringMotor(1, cardRoot, "GroupTransparency")
    setTrans(0)

    -- Header
    local header = Creator.New("Frame", {
        Size = UDim2.new(1, 0, 0, 70),
        BackgroundTransparency = 1,
        Parent = cardRoot
    }, {
        Creator.New("ImageLabel", {
            Size = UDim2.fromOffset(36, 36),
            Position = UDim2.new(0, 24, 0, 18),
            BackgroundTransparency = 1,
            Image = WindUI:GetIcon("solar/shield-keyhole-bold").Image or "rbxassetid://10734951847",
            ThemeTag = { ImageColor3 = "Accent" }
        }),
        Creator.New("TextLabel", {
            FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.Bold),
            Text = self.Title,
            TextSize = 20,
            TextXAlignment = Enum.TextXAlignment.Left,
            Size = UDim2.new(1, -80, 0, 22),
            Position = UDim2.new(0, 72, 0, 16),
            BackgroundTransparency = 1,
            ThemeTag = { TextColor3 = "Text" }
        }),
        Creator.New("TextLabel", {
            FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.Medium),
            Text = self.SubTitle,
            TextSize = 13,
            TextXAlignment = Enum.TextXAlignment.Left,
            Size = UDim2.new(1, -80, 0, 16),
            Position = UDim2.new(0, 72, 0, 40),
            BackgroundTransparency = 1,
            ThemeTag = { TextColor3 = "SubText" }
        })
    })

    -- Note label
    Creator.New("TextLabel", {
        FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.Regular),
        Text = self.Note,
        TextSize = 12,
        TextXAlignment = Enum.TextXAlignment.Center,
        Size = UDim2.new(1, -48, 0, 30),
        Position = UDim2.new(0, 24, 0, 75),
        BackgroundTransparency = 1,
        TextWrapped = true,
        ThemeTag = { TextColor3 = "SubText" },
        Parent = cardRoot
    })

    -- Input box
    local inputWrap = Creator.New("Frame", {
        Size = UDim2.new(1, -48, 0, 42),
        Position = UDim2.new(0, 24, 0, 115),
        ThemeTag = { BackgroundColor3 = "Input" },
        Parent = cardRoot
    }, {
        Creator.New("UICorner", { CornerRadius = UDim.new(0, 8) }),
        Creator.New("UIStroke", {
            Name = "InputStroke",
            Transparency = 0.5,
            Thickness = 1,
            ThemeTag = { Color = "InElementBorder" }
        })
    })

    local keyInput = Creator.New("TextBox", {
        FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.Medium),
        PlaceholderText = "Paste or type your key here...",
        Text = "",
        TextSize = 14,
        TextColor3 = Color3.fromRGB(240, 240, 240),
        PlaceholderColor3 = Color3.fromRGB(140, 140, 140),
        Size = UDim2.new(1, -30, 1, 0),
        Position = UDim2.new(0, 15, 0, 0),
        BackgroundTransparency = 1,
        ClearTextOnFocus = false,
        TextXAlignment = Enum.TextXAlignment.Left,
        ThemeTag = { TextColor3 = "Text" },
        Parent = inputWrap
    })

    -- Buttons row
    local btnRow = Creator.New("Frame", {
        Size = UDim2.new(1, -48, 0, 42),
        Position = UDim2.new(0, 24, 0, 175),
        BackgroundTransparency = 1,
        Parent = cardRoot
    })

    local function createBtn(text, iconSpec, posScale, sizeScale, isAccent, callback)
        local btn = Creator.New("TextButton", {
            Text = "",
            Size = sizeScale,
            Position = posScale,
            ThemeTag = { BackgroundColor3 = isAccent and "Accent" or "Element" },
            Parent = btnRow
        }, {
            Creator.New("UICorner", { CornerRadius = UDim.new(0, 8) }),
            Creator.New("UIStroke", {
                Transparency = isAccent and 0.2 or 0.6,
                Thickness = 1,
                ThemeTag = { Color = isAccent and "Accent" or "ElementBorder" }
            })
        })
        
        local label = Creator.New("TextLabel", {
            FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.SemiBold),
            Text = text,
            TextSize = 13,
            Size = UDim2.fromScale(1, 1),
            BackgroundTransparency = 1,
            ThemeTag = { TextColor3 = isAccent and "ToggleToggled" or "Text" },
            Parent = btn
        })
        
        if iconSpec then
            local ico = Creator.New("ImageLabel", {
                Size = UDim2.fromOffset(16, 16),
                Position = UDim2.new(0, 14, 0.5, -8),
                BackgroundTransparency = 1,
                Image = WindUI:GetIcon(iconSpec).Image or "",
                ThemeTag = { ImageColor3 = isAccent and "ToggleToggled" or "Text" },
                Parent = btn
            })
            label.Position = UDim2.new(0, 14, 0, 0)
        end

        btn.MouseButton1Click:Connect(function()
            pcall(callback)
        end)
        return btn
    end

    createBtn("Get Key", "solar/link-bold", UDim2.new(0, 0, 0, 0), UDim2.new(0.3, -6, 1, 0), false, function()
        if self.GetKeyURL and self.GetKeyURL ~= "" then
            local url = self.GetKeyURL
            if setclipboard then
                setclipboard(url)
                if WindUI.Notify then
                    WindUI:Notify({ Title = "Key System", Content = "Copied GetKey URL to clipboard!", Type = "Info", Duration = 4 })
                end
            end
            pcall(function()
                if openurl then openurl(url)
                elseif syn and syn.request then syn.request({ Url = url, Method = "GET" }) end
            end)
        end
    end)

    createBtn("Paste", "solar/clipboard-bold", UDim2.new(0.3, 2, 0, 0), UDim2.new(0.3, -6, 1, 0), false, function()
        if getclipboard then
            local clip = getclipboard()
            if clip and type(clip) == "string" then
                keyInput.Text = clip
            end
        end
    end)

    local verifyBtn = createBtn("Unlock", "solar/check-circle-bold", UDim2.new(0.6, 4, 0, 0), UDim2.new(0.4, -4, 1, 0), true, function()
        local ok = self:VerifyKey(keyInput.Text, false)
        if ok then
            if WindUI.Notify then
                WindUI:Notify({ Title = "Verification Success", Content = "Access granted! Welcome to WindUI Ultimate.", Type = "Success", Duration = 4 })
            end
            setTrans(1)
            setScale(1.15)
            setTint(1)
            task.wait(0.35)
            tint:Destroy()
        else
            if WindUI.Notify then
                WindUI:Notify({ Title = "Verification Failed", Content = "Invalid key entered. Please verify and try again.", Type = "Error", Duration = 4 })
            end
            -- Shake animation
            local origPos = cardRoot.Position
            for i = 1, 5 do
                cardRoot.Position = origPos + UDim2.fromOffset(math.random(-8, 8), 0)
                task.wait(0.04)
            end
            cardRoot.Position = origPos
        end
    end)
end

WindUI.KeySystem = KeySystem
""")
print("Part 5 added.")

# PART 6: Notification API
code_parts.append("""
--[[
================================================================================
    Notification System
================================================================================
--]]
local NotificationAPI = {
    _holder = nil,
    _activeNotifications = {}
}

function NotificationAPI.Init()
    if NotificationAPI._holder then return end
    local gui = WindUI.PopupGUI
    if not gui then return end
    
    local holder = Creator.New("Frame", {
        Name = "WindUINotificationHolder",
        Position = UDim2.new(1, -330, 1, -24),
        Size = UDim2.new(0, 310, 1, -24),
        AnchorPoint = Vector2.new(1, 1),
        BackgroundTransparency = 1,
        Parent = gui
    }, {
        Creator.New("UIListLayout", {
            HorizontalAlignment = Enum.HorizontalAlignment.Center,
            SortOrder = Enum.SortOrder.LayoutOrder,
            VerticalAlignment = Enum.VerticalAlignment.Bottom,
            Padding = UDim.new(0, 12)
        })
    })
    NotificationAPI._holder = holder
end

function NotificationAPI.New(config)
    NotificationAPI.Init()
    config = config or {}
    local title = config.Title or "Notification"
    local content = config.Content or ""
    local subContent = config.SubContent or ""
    local notifType = config.Type or "Info" -- Info, Success, Warning, Error
    local duration = config.Duration or 5
    local buttons = config.Buttons or {}
    
    local notif = { Closed = false }
    local cardPaint = AcrylicEngine.AcrylicPaint()
    
    local stripeColor = Color3.fromRGB(90, 165, 255)
    if notifType == "Success" then stripeColor = Color3.fromRGB(45, 215, 130)
    elseif notifType == "Warning" then stripeColor = Color3.fromRGB(255, 170, 40)
    elseif notifType == "Error" then stripeColor = Color3.fromRGB(220, 50, 70) end

    local stripe = Creator.New("Frame", {
        Size = UDim2.new(0, 3, 1, -16),
        Position = UDim2.new(0, 6, 0, 8),
        BackgroundColor3 = stripeColor,
        BorderSizePixel = 0,
        ZIndex = 5
    }, { Creator.New("UICorner", { CornerRadius = UDim.new(1, 0) }) })

    local titleLbl = Creator.New("TextLabel", {
        FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.Bold),
        Text = title,
        TextSize = 14,
        TextXAlignment = Enum.TextXAlignment.Left,
        Size = UDim2.new(1, -50, 0, 18),
        Position = UDim2.new(0, 18, 0, 12),
        BackgroundTransparency = 1,
        ThemeTag = { TextColor3 = "Text" },
        ZIndex = 5
    })

    local contentLbl = Creator.New("TextLabel", {
        FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.Medium),
        Text = content,
        TextSize = 13,
        TextXAlignment = Enum.TextXAlignment.Left,
        AutomaticSize = Enum.AutomaticSize.Y,
        Size = UDim2.new(1, -36, 0, 0),
        Position = UDim2.new(0, 18, 0, 32),
        BackgroundTransparency = 1,
        TextWrapped = true,
        ThemeTag = { TextColor3 = "SubText" },
        ZIndex = 5
    })

    local subContentLbl = Creator.New("TextLabel", {
        FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.Regular),
        Text = subContent,
        TextSize = 11,
        TextXAlignment = Enum.TextXAlignment.Left,
        AutomaticSize = Enum.AutomaticSize.Y,
        Size = UDim2.new(1, -36, 0, 0),
        Position = UDim2.new(0, 18, 0, 50),
        BackgroundTransparency = 1,
        TextWrapped = true,
        ThemeTag = { TextColor3 = "SubText" },
        Visible = (subContent ~= ""),
        ZIndex = 5
    })

    local closeBtn = Creator.New("TextButton", {
        Text = "",
        Position = UDim2.new(1, -12, 0, 12),
        Size = UDim2.fromOffset(20, 20),
        AnchorPoint = Vector2.new(1, 0),
        BackgroundTransparency = 1,
        ZIndex = 6
    }, {
        Creator.New("ImageLabel", {
            Image = WindUI:GetIcon("lucide-x").Image or "rbxassetid://10747384394",
            Size = UDim2.fromOffset(14, 14),
            Position = UDim2.fromScale(0.5, 0.5),
            AnchorPoint = Vector2.new(0.5, 0.5),
            BackgroundTransparency = 1,
            ThemeTag = { ImageColor3 = "SubText" }
        })
    })

    local notifRoot = Creator.New("Frame", {
        Size = UDim2.new(1, 0, 1, 0),
        Position = UDim2.fromScale(1.1, 0),
        BackgroundTransparency = 1
    }, {
        cardPaint.Frame,
        stripe,
        titleLbl,
        contentLbl,
        subContentLbl,
        closeBtn
    })

    local containerHeight = 65
    if content ~= "" then containerHeight = containerHeight + 14 end
    if subContent ~= "" then containerHeight = containerHeight + 16 end
    if #buttons > 0 then
        containerHeight = containerHeight + 36
        local btnContainer = Creator.New("Frame", {
            Size = UDim2.new(1, -36, 0, 30),
            Position = UDim2.new(0, 18, 1, -38),
            BackgroundTransparency = 1,
            ZIndex = 5
        }, {
            Creator.New("UIListLayout", {
                FillDirection = Enum.FillDirection.Horizontal,
                HorizontalAlignment = Enum.HorizontalAlignment.Right,
                SortOrder = Enum.SortOrder.LayoutOrder,
                Padding = UDim.new(0, 8)
            })
        })
        for idx, bCfg in ipairs(buttons) do
            local bTitle = bCfg.Title or "Button"
            local bCb = bCfg.Callback or function() end
            local nBtn = Creator.New("TextButton", {
                Text = bTitle,
                FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.SemiBold),
                TextSize = 12,
                Size = UDim2.fromOffset(75, 28),
                ThemeTag = { BackgroundColor3 = "Element", TextColor3 = "Text" },
                Parent = btnContainer,
                ZIndex = 6
            }, {
                Creator.New("UICorner", { CornerRadius = UDim.new(0, 6) }),
                Creator.New("UIStroke", { Thickness = 1, Transparency = 0.6, ThemeTag = { Color = "ElementBorder" } })
            })
            nBtn.MouseButton1Click:Connect(function()
                pcall(bCb)
                notif:Close()
            end)
        end
        notifRoot.Parent = Creator.New("Frame", { Size = UDim2.fromScale(1, 1), BackgroundTransparency = 1 }, { btnContainer })
    end

    local holderWrap = Creator.New("Frame", {
        Size = UDim2.new(1, 0, 0, containerHeight),
        BackgroundTransparency = 1,
        Parent = NotificationAPI._holder
    }, { notifRoot })

    local motor = SingleMotor.new(1.1, true)
    motor:OnStep(function(val)
        if notifRoot and notifRoot.Parent then
            notifRoot.Position = UDim2.fromScale(val, 0)
        end
    end)

    function notif:Open()
        motor:SetGoal(Spring.new(0, { frequency = 5, dampingRatio = 0.9 }))
    end

    function notif:Close()
        if self.Closed then return end
        self.Closed = true
        motor:SetGoal(Spring.new(1.1, { frequency = 6, dampingRatio = 0.9 }))
        task.delay(0.35, function()
            pcall(function()
                if cardPaint.Model then cardPaint.Model:Destroy() end
                holderWrap:Destroy()
            end)
        end)
    end

    closeBtn.MouseButton1Click:Connect(function() notif:Close() end)
    notif:Open()

    if duration and duration > 0 then
        task.delay(duration, function()
            notif:Close()
        end)
    end

    return notif
end

function WindUI:Notify(config)
    return NotificationAPI.New(config)
end
""")
print("Part 6 added.")

# PART 7: Dialog Popup System
code_parts.append("""
--[[
================================================================================
    Dialog Popup System
================================================================================
--]]
local DialogAPI = {}
DialogAPI.__index = DialogAPI

function DialogAPI.New(windowInstance, config)
    config = config or {}
    local title = config.Title or "Dialog"
    local content = config.Content or ""
    local buttons = config.Buttons or { { Title = "OK", Callback = function() end } }
    
    local gui = WindUI.PopupGUI
    if not gui then return end

    local tint = Creator.New("TextButton", {
        Name = "DialogTint",
        Text = "",
        Size = UDim2.fromScale(1, 1),
        BackgroundColor3 = Color3.fromRGB(0, 0, 0),
        BackgroundTransparency = 1,
        Parent = gui
    })
    local tintMotor, setTint = Creator.SpringMotor(1, tint, "BackgroundTransparency")
    setTint(0.4)

    local scaleHolder = Creator.New("UIScale", { Scale = 0.85 })
    local scaleMotor, setScale = Creator.SpringMotor(0.85, scaleHolder, "Scale")
    setScale(1)

    local cardPaint = AcrylicEngine.AcrylicPaint()
    local cardRoot = Creator.New("CanvasGroup", {
        Name = "DialogCard",
        Size = UDim2.fromOffset(360, 180),
        AnchorPoint = Vector2.new(0.5, 0.5),
        Position = UDim2.fromScale(0.5, 0.5),
        GroupTransparency = 1,
        Parent = tint
    }, {
        Creator.New("UICorner", { CornerRadius = UDim.new(0, 10) }),
        Creator.New("UIStroke", { Thickness = 1, Transparency = 0.4, ThemeTag = { Color = "DialogBorder" } }),
        scaleHolder,
        cardPaint.Frame
    })
    local transMotor, setTrans = Creator.SpringMotor(1, cardRoot, "GroupTransparency")
    setTrans(0)

    -- Header
    Creator.New("TextLabel", {
        FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.Bold),
        Text = title,
        TextSize = 18,
        TextXAlignment = Enum.TextXAlignment.Left,
        Size = UDim2.new(1, -40, 0, 24),
        Position = UDim2.new(0, 20, 0, 18),
        BackgroundTransparency = 1,
        ThemeTag = { TextColor3 = "Text" },
        Parent = cardRoot
    })

    -- Content
    local contentLbl = Creator.New("TextLabel", {
        FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.Medium),
        Text = content,
        TextSize = 13,
        TextXAlignment = Enum.TextXAlignment.Left,
        TextYAlignment = Enum.TextYAlignment.Top,
        AutomaticSize = Enum.AutomaticSize.Y,
        Size = UDim2.new(1, -40, 0, 60),
        Position = UDim2.new(0, 20, 0, 52),
        BackgroundTransparency = 1,
        TextWrapped = true,
        ThemeTag = { TextColor3 = "SubText" },
        Parent = cardRoot
    })

    -- Button Holder
    local btnHolder = Creator.New("Frame", {
        Size = UDim2.new(1, -40, 0, 36),
        Position = UDim2.new(0, 20, 1, -50),
        BackgroundTransparency = 1,
        Parent = cardRoot
    }, {
        Creator.New("UIListLayout", {
            FillDirection = Enum.FillDirection.Horizontal,
            HorizontalAlignment = Enum.HorizontalAlignment.Right,
            SortOrder = Enum.SortOrder.LayoutOrder,
            Padding = UDim.new(0, 10)
        })
    })

    local dialogObj = { Closed = false }
    function dialogObj:Close()
        if self.Closed then return end
        self.Closed = true
        setTrans(1)
        setScale(1.15)
        setTint(1)
        task.delay(0.35, function()
            pcall(function()
                if cardPaint.Model then cardPaint.Model:Destroy() end
                tint:Destroy()
            end)
        end)
    end

    local count = #buttons
    for i, bCfg in ipairs(buttons) do
        local bTitle = bCfg.Title or "Button"
        local bCb = bCfg.Callback or function() end
        local isAccent = (i == count)
        local btn = Creator.New("TextButton", {
            Text = bTitle,
            FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.SemiBold),
            TextSize = 13,
            Size = UDim2.new(1 / count, -((count - 1) * 10 / count), 1, 0),
            ThemeTag = { BackgroundColor3 = isAccent and "Accent" or "Element", TextColor3 = isAccent and "ToggleToggled" or "Text" },
            Parent = btnHolder
        }, {
            Creator.New("UICorner", { CornerRadius = UDim.new(0, 6) }),
            Creator.New("UIStroke", {
                Thickness = 1,
                Transparency = isAccent and 0.2 or 0.6,
                ThemeTag = { Color = isAccent and "Accent" or "ElementBorder" }
            })
        })
        btn.MouseButton1Click:Connect(function()
            pcall(bCb)
            dialogObj:Close()
        end)
    end

    return dialogObj
end

function WindUI:CreateDialog(config)
    return DialogAPI.New(self.Window, config)
end
""")
print("Part 7 added.")

# PART 8: Window & Sidebar Navigation System
code_parts.append("""
--[[
================================================================================
    Window & Sidebar Navigation System
================================================================================
--]]
local WindowAPI = {}
WindowAPI.__index = WindowAPI

function WindowAPI.New(config)
    config = config or {}
    local title = config.Title or "WindUI Ultimate"
    local subTitle = config.SubTitle or "v2.0"
    local tabWidth = config.TabWidth or 170
    local size = config.Size or UDim2.fromOffset(640, 460)
    local useAcrylic = (config.Acrylic ~= false)
    local theme = config.Theme or "Blood Red"
    local keySystemEnabled = config.KeySystem or false
    local keySettings = config.KeySettings or {}

    WindUI.UseAcrylic = useAcrylic
    WindUI.Theme = theme

    local win = setmetatable({}, WindowAPI)
    win.Tabs = {}
    win.TabGroups = {}
    win.AllElements = {}
    win.ActiveTab = nil
    win.IsMinimized = false
    win.IsDragging = false

    -- Create Root Acrylic Paint
    local mainPaint = AcrylicEngine.AcrylicPaint()
    local rootFrame = Creator.New("CanvasGroup", {
        Name = "WindUIMainWindow",
        Size = size,
        AnchorPoint = Vector2.new(0.5, 0.5),
        Position = UDim2.fromScale(0.5, 0.5),
        GroupTransparency = 1,
        Parent = WindUI.GUI,
        Visible = false
    }, {
        Creator.New("UICorner", { CornerRadius = UDim.new(0, 12) }),
        Creator.New("UIStroke", { Thickness = 1.2, Transparency = 0.35, ThemeTag = { Color = "AcrylicBorder" } }),
        mainPaint.Frame
    })
    win.Root = rootFrame
    win.AcrylicPaint = mainPaint

    -- Scale & Opacity Motors
    local scaleHolder = Creator.New("UIScale", { Scale = 0.9 })
    scaleHolder.Parent = rootFrame
    local scaleMotor, setScale = Creator.SpringMotor(0.9, scaleHolder, "Scale")
    local transMotor, setTrans = Creator.SpringMotor(1, rootFrame, "GroupTransparency")

    -- Title Bar
    local titleBar = Creator.New("Frame", {
        Name = "TitleBar",
        Size = UDim2.new(1, 0, 0, 48),
        BackgroundTransparency = 1,
        Parent = rootFrame
    }, {
        Creator.New("Frame", {
            Name = "Line",
            Size = UDim2.new(1, 0, 0, 1),
            Position = UDim2.new(0, 0, 1, -1),
            BorderSizePixel = 0,
            ThemeTag = { BackgroundColor3 = "TitleBarLine" }
        }),
        Creator.New("ImageLabel", {
            Name = "Logo",
            Size = UDim2.fromOffset(24, 24),
            Position = UDim2.new(0, 16, 0.5, -12),
            BackgroundTransparency = 1,
            Image = config.Icon and (WindUI:GetIcon(config.Icon).Image or "") or "rbxassetid://10734982144",
            ThemeTag = { ImageColor3 = "Accent" }
        }),
        Creator.New("TextLabel", {
            Name = "Title",
            FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.Bold),
            Text = title,
            TextSize = 15,
            TextXAlignment = Enum.TextXAlignment.Left,
            Size = UDim2.new(0, 200, 0, 18),
            Position = UDim2.new(0, 48, 0, 8),
            BackgroundTransparency = 1,
            ThemeTag = { TextColor3 = "Text" }
        }),
        Creator.New("TextLabel", {
            Name = "SubTitle",
            FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.Medium),
            Text = subTitle,
            TextSize = 11,
            TextXAlignment = Enum.TextXAlignment.Left,
            Size = UDim2.new(0, 200, 0, 14),
            Position = UDim2.new(0, 48, 0, 26),
            BackgroundTransparency = 1,
            ThemeTag = { TextColor3 = "SubText" }
        })
    })
    win.TitleBar = titleBar

    -- Dragging Logic
    local dragToggle = nil
    local dragSpeed = 0.18
    local dragStart = nil
    local startPos = nil

    titleBar.InputBegan:Connect(function(inp)
        if (inp.UserInputType == Enum.UserInputType.MouseButton1 or inp.UserInputType == Enum.UserInputType.Touch) then
            win.IsDragging = true
            dragStart = inp.Position
            startPos = rootFrame.Position
            inp.Changed:Connect(function()
                if inp.UserInputState == Enum.UserInputState.End then
                    win.IsDragging = false
                end
            end)
        end
    end)

    titleBar.InputChanged:Connect(function(inp)
        if inp.UserInputType == Enum.UserInputType.MouseMovement or inp.UserInputType == Enum.UserInputType.Touch then
            dragToggle = inp
        end
    end)

    Services.UserInputService.InputChanged:Connect(function(inp)
        if inp == dragToggle and win.IsDragging then
            local delta = inp.Position - dragStart
            local goalPos = UDim2.new(startPos.X.Scale, startPos.X.Offset + delta.X, startPos.Y.Scale, startPos.Y.Offset + delta.Y)
            rootFrame.Position = goalPos
        end
    end)

    -- Floating Minimize Pill / Button
    local floatingPill = Creator.New("TextButton", {
        Name = "WindUIFloatingMinimize",
        Text = "",
        Size = UDim2.fromOffset(130, 38),
        Position = UDim2.new(0, 30, 0, 30),
        BackgroundColor3 = Color3.fromRGB(15, 15, 22),
        Visible = false,
        Parent = WindUI.GUI
    }, {
        Creator.New("UICorner", { CornerRadius = UDim.new(1, 0) }),
        Creator.New("UIStroke", { Thickness = 1.5, ThemeTag = { Color = "Accent" } }),
        Creator.New("ImageLabel", {
            Size = UDim2.fromOffset(20, 20),
            Position = UDim2.new(0, 12, 0.5, -10),
            BackgroundTransparency = 1,
            Image = config.Icon and (WindUI:GetIcon(config.Icon).Image or "") or "rbxassetid://10734982144",
            ThemeTag = { ImageColor3 = "Accent" }
        }),
        Creator.New("TextLabel", {
            FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.Bold),
            Text = "Restore UI",
            TextSize = 12,
            Size = UDim2.new(1, -44, 1, 0),
            Position = UDim2.new(0, 38, 0, 0),
            BackgroundTransparency = 1,
            TextXAlignment = Enum.TextXAlignment.Left,
            ThemeTag = { TextColor3 = "Text" }
        })
    })

    -- Floating Pill Drag
    local pillDragging, pillStart, pillStartPos = false, nil, nil
    floatingPill.InputBegan:Connect(function(inp)
        if inp.UserInputType == Enum.UserInputType.MouseButton1 or inp.UserInputType == Enum.UserInputType.Touch then
            pillDragging = true
            pillStart = inp.Position
            pillStartPos = floatingPill.Position
        end
    end)
    Services.UserInputService.InputEnded:Connect(function(inp)
        if inp.UserInputType == Enum.UserInputType.MouseButton1 or inp.UserInputType == Enum.UserInputType.Touch then
            pillDragging = false
        end
    end)
    Services.UserInputService.InputChanged:Connect(function(inp)
        if pillDragging and (inp.UserInputType == Enum.UserInputType.MouseMovement or inp.UserInputType == Enum.UserInputType.Touch) then
            local delta = inp.Position - pillStart
            floatingPill.Position = UDim2.new(pillStartPos.X.Scale, pillStartPos.X.Offset + delta.X, pillStartPos.Y.Scale, pillStartPos.Y.Offset + delta.Y)
        end
    end)

    -- Window Controls (Minimize & Close)
    local ctrlHolder = Creator.New("Frame", {
        Size = UDim2.fromOffset(70, 32),
        Position = UDim2.new(1, -80, 0.5, -16),
        BackgroundTransparency = 1,
        Parent = titleBar
    }, {
        Creator.New("UIListLayout", {
            FillDirection = Enum.FillDirection.Horizontal,
            HorizontalAlignment = Enum.HorizontalAlignment.Right,
            SortOrder = Enum.SortOrder.LayoutOrder,
            Padding = UDim.new(0, 6)
        })
    })

    function win:Minimize()
        win.IsMinimized = true
        setScale(0.85)
        setTrans(1)
        task.delay(0.25, function()
            rootFrame.Visible = false
            floatingPill.Visible = true
        end)
        if WindUI.Notify then
            WindUI:Notify({ Title = "UI Minimized", Content = "Click the floating pill or press " .. tostring(WindUI.MinimizeKey:math("KeyCode.") or WindUI.MinimizeKey.Name) .. " to restore.", Type = "Info", Duration = 3 })
        end
    end

    function win:Restore()
        win.IsMinimized = false
        floatingPill.Visible = false
        rootFrame.Visible = true
        setScale(1)
        setTrans(0)
    end

    function win:ToggleMinimize()
        if win.IsMinimized then win:Restore() else win:Minimize() end
    end

    floatingPill.MouseButton1Click:Connect(function()
        if not pillDragging then win:Restore() end
    end)

    local minBtn = Creator.New("TextButton", {
        Text = "", Size = UDim2.fromOffset(28, 28), ThemeTag = { BackgroundColor3 = "Element" }, Parent = ctrlHolder
    }, {
        Creator.New("UICorner", { CornerRadius = UDim.new(0, 6) }),
        Creator.New("ImageLabel", {
            Size = UDim2.fromOffset(14, 14), Position = UDim2.fromScale(0.5, 0.5), AnchorPoint = Vector2.new(0.5, 0.5),
            BackgroundTransparency = 1, Image = WindUI:GetIcon("lucide-minus").Image or "rbxassetid://10734896206",
            ThemeTag = { ImageColor3 = "Text" }
        })
    })
    minBtn.MouseButton1Click:Connect(function() win:Minimize() end)

    local closeBtn = Creator.New("TextButton", {
        Text = "", Size = UDim2.fromOffset(28, 28), ThemeTag = { BackgroundColor3 = "Element" }, Parent = ctrlHolder
    }, {
        Creator.New("UICorner", { CornerRadius = UDim.new(0, 6) }),
        Creator.New("ImageLabel", {
            Size = UDim2.fromOffset(14, 14), Position = UDim2.fromScale(0.5, 0.5), AnchorPoint = Vector2.new(0.5, 0.5),
            BackgroundTransparency = 1, Image = WindUI:GetIcon("lucide-x").Image or "rbxassetid://10747384394",
            ThemeTag = { ImageColor3 = "Text" }
        })
    })
    closeBtn.MouseButton1Click:Connect(function()
        WindUI:Destroy()
    end)

    -- Listen for Minimize Key
    Services.UserInputService.InputBegan:Connect(function(inp, gpe)
        if not gpe and inp.KeyCode == WindUI.MinimizeKey then
            win:ToggleMinimize()
        end
    end)

    -- Sidebar Area
    local sidebar = Creator.New("Frame", {
        Name = "Sidebar",
        Size = UDim2.new(0, tabWidth, 1, -48),
        Position = UDim2.new(0, 0, 0, 48),
        BackgroundTransparency = 1,
        Parent = rootFrame
    }, {
        Creator.New("Frame", {
            Name = "SideLine",
            Size = UDim2.new(0, 1, 1, 0),
            Position = UDim2.new(1, -1, 0, 0),
            BorderSizePixel = 0,
            ThemeTag = { BackgroundColor3 = "TitleBarLine" }
        })
    })
    win.Sidebar = sidebar

    -- Search Box inside Sidebar Header
    local searchWrap = Creator.New("Frame", {
        Size = UDim2.new(1, -20, 0, 32),
        Position = UDim2.new(0, 10, 0, 10),
        ThemeTag = { BackgroundColor3 = "Input" },
        Parent = sidebar
    }, {
        Creator.New("UICorner", { CornerRadius = UDim.new(0, 6) }),
        Creator.New("UIStroke", { Thickness = 1, Transparency = 0.5, ThemeTag = { Color = "InElementBorder" } }),
        Creator.New("ImageLabel", {
            Size = UDim2.fromOffset(14, 14), Position = UDim2.new(0, 10, 0.5, -7), BackgroundTransparency = 1,
            Image = WindUI:GetIcon("lucide-search").Image or "rbxassetid://10734943674",
            ThemeTag = { ImageColor3 = "SubText" }
        })
    })

    local searchBox = Creator.New("TextBox", {
        FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.Medium),
        PlaceholderText = "Search features...",
        Text = "", TextSize = 12, Size = UDim2.new(1, -34, 1, 0), Position = UDim2.new(0, 30, 0, 0),
        BackgroundTransparency = 1, ClearTextOnFocus = false, TextXAlignment = Enum.TextXAlignment.Left,
        ThemeTag = { TextColor3 = "Text", PlaceholderColor3 = "SubText" },
        Parent = searchWrap
    })

    searchBox:GetPropertyChangedSignal("Text"):Connect(function()
        local query = tostring(searchBox.Text):lower():gsub("^%s+", ""):gsub("%s+$", "")
        if query == "" then
            -- Restore active tab
            for _, tab in ipairs(win.Tabs) do
                if tab == win.ActiveTab then tab.Container.Visible = true else tab.Container.Visible = false end
            end
            for elemFrame, _ in pairs(win.AllElements) do
                if elemFrame and elemFrame.Parent then elemFrame.Visible = true end
            end
        else
            -- Show search results across current tab elements
            if win.ActiveTab then
                for elemFrame, elemTitle in pairs(win.AllElements) do
                    if elemFrame and elemFrame:IsDescendantOf(win.ActiveTab.Container) then
                        if elemTitle:find(query, 1, true) then
                            elemFrame.Visible = true
                        else
                            elemFrame.Visible = false
                        end
                    end
                end
            end
        end
    end)

    -- Sidebar Scrollable Tabs Holder ("Bisa di Scroll jika kebanyakan Fitur/Tab")
    local tabScroll = Creator.New("ScrollingFrame", {
        Name = "SidebarTabScroll",
        Size = UDim2.new(1, 0, 1, -54),
        Position = UDim2.new(0, 0, 0, 52),
        BackgroundTransparency = 1,
        BorderSizePixel = 0,
        ScrollBarThickness = 3,
        CanvasSize = UDim2.new(0, 0, 0, 0),
        AutomaticCanvasSize = Enum.AutomaticSize.Y,
        ThemeTag = { ScrollBarImageColor3 = "SubText" },
        Parent = sidebar
    }, {
        Creator.New("UIListLayout", {
            SortOrder = Enum.SortOrder.LayoutOrder,
            Padding = UDim.new(0, 4)
        }),
        Creator.New("UIPadding", {
            PaddingLeft = UDim.new(0, 10), PaddingRight = UDim.new(0, 10),
            PaddingTop = UDim.new(0, 4), PaddingBottom = UDim.new(0, 14)
        })
    })
    win.TabScroll = tabScroll

    -- Content Area Holder
    local contentArea = Creator.New("Frame", {
        Name = "ContentArea",
        Size = UDim2.new(1, -tabWidth, 1, -48),
        Position = UDim2.new(0, tabWidth, 0, 48),
        BackgroundTransparency = 1,
        Parent = rootFrame
    })
    win.ContentArea = contentArea

    -- Unlock logic via Key System or Direct
    function win:OpenWindow()
        rootFrame.Visible = true
        setScale(1)
        setTrans(0)
        Animation.Apply(WindUI.Theme, rootFrame)
    end

    if keySystemEnabled then
        local ks = KeySystem.Init(win, keySettings)
        ks:Render(function()
            win:OpenWindow()
        end)
    else
        win:OpenWindow()
    end

    -- AddTab & Accordion Sidebar Dropdowns ("DropDown Di Samping")
    function win:AddTabGroup(groupConfig)
        groupConfig = groupConfig or {}
        local groupTitle = groupConfig.Title or "Category"
        local groupIcon = groupConfig.Icon

        local groupWrap = Creator.New("Frame", {
            Size = UDim2.new(1, 0, 0, 32),
            BackgroundTransparency = 1,
            AutomaticSize = Enum.AutomaticSize.Y,
            Parent = tabScroll
        }, {
            Creator.New("UIListLayout", { SortOrder = Enum.SortOrder.LayoutOrder, Padding = UDim.new(0, 3) })
        })

        local groupHeader = Creator.New("TextButton", {
            Text = "", Size = UDim2.new(1, 0, 0, 32), BackgroundTransparency = 1, Parent = groupWrap
        })
        local groupArrow = Creator.New("ImageLabel", {
            Size = UDim2.fromOffset(14, 14), Position = UDim2.new(1, -18, 0.5, -7), BackgroundTransparency = 1,
            Image = WindUI:GetIcon("lucide-chevron-down").Image or "rbxassetid://10709790948",
            ThemeTag = { ImageColor3 = "SubText" }, Parent = groupHeader
        })
        Creator.New("TextLabel", {
            FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.Bold),
            Text = groupTitle:upper(), TextSize = 11, Size = UDim2.new(1, -50, 1, 0),
            Position = UDim2.new(0, groupIcon and 30 or 6, 0, 0), BackgroundTransparency = 1,
            TextXAlignment = Enum.TextXAlignment.Left, ThemeTag = { TextColor3 = "SubText" }, Parent = groupHeader
        })
        if groupIcon then
            Creator.New("ImageLabel", {
                Size = UDim2.fromOffset(16, 16), Position = UDim2.new(0, 6, 0.5, -8), BackgroundTransparency = 1,
                Image = WindUI:GetIcon(groupIcon).Image or "", ThemeTag = { ImageColor3 = "SubText" }, Parent = groupHeader
            })
        end

        local subContainer = Creator.New("Frame", {
            Size = UDim2.new(1, 0, 0, 0), BackgroundTransparency = 1, AutomaticSize = Enum.AutomaticSize.Y,
            Visible = true, Parent = groupWrap
        }, {
            Creator.New("UIListLayout", { SortOrder = Enum.SortOrder.LayoutOrder, Padding = UDim.new(0, 3) }),
            Creator.New("UIPadding", { PaddingLeft = UDim.new(0, 12) })
        })

        local isOpen = true
        groupHeader.MouseButton1Click:Connect(function()
            isOpen = not isOpen
            subContainer.Visible = isOpen
            groupArrow.Rotation = isOpen and 0 or -90
        end)

        return {
            Container = subContainer,
            AddTab = function(selfGroup, tabConfig)
                return win:AddTab(tabConfig, subContainer)
            end
        }
    end

    function win:AddTab(tabConfig, parentHolder)
        tabConfig = tabConfig or {}
        local tabTitle = (type(tabConfig) == "string" and tabConfig) or tabConfig.Title or "Tab"
        local tabIcon = (type(tabConfig) == "table" and tabConfig.Icon) or nil

        local tabBtn = Creator.New("TextButton", {
            Text = "", Size = UDim2.new(1, 0, 0, 34), BackgroundTransparency = 1,
            Parent = parentHolder or tabScroll
        }, { Creator.New("UICorner", { CornerRadius = UDim.new(0, 8) }) })

        local tabBgMotor, setTabBg = Creator.SpringMotor(1, tabBtn, "BackgroundTransparency")
        local titleLbl = Creator.New("TextLabel", {
            FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.Medium),
            Text = tabTitle, TextSize = 13, Size = UDim2.new(1, -40, 1, 0),
            Position = UDim2.new(0, tabIcon and 34 or 12, 0, 0), BackgroundTransparency = 1,
            TextXAlignment = Enum.TextXAlignment.Left, ThemeTag = { TextColor3 = "SubText" }, Parent = tabBtn
        })
        local icoLbl = nil
        if tabIcon then
            icoLbl = Creator.New("ImageLabel", {
                Size = UDim2.fromOffset(16, 16), Position = UDim2.new(0, 10, 0.5, -8), BackgroundTransparency = 1,
                Image = WindUI:GetIcon(tabIcon).Image or "", ThemeTag = { ImageColor3 = "SubText" }, Parent = tabBtn
            })
        end

        local activeIndicator = Creator.New("Frame", {
            Size = UDim2.new(0, 3, 0.6, 0), Position = UDim2.new(0, 2, 0.2, 0), BackgroundTransparency = 1,
            ThemeTag = { BackgroundColor3 = "Accent" }, Parent = tabBtn
        }, { Creator.New("UICorner", { CornerRadius = UDim.new(1, 0) }) })
        local indMotor, setInd = Creator.SpringMotor(1, activeIndicator, "BackgroundTransparency")

        -- Content Scrollable Page for Tab
        local pageScroll = Creator.New("ScrollingFrame", {
            Name = "Page_" .. tabTitle,
            Size = UDim2.fromScale(1, 1), BackgroundTransparency = 1, BorderSizePixel = 0,
            ScrollBarThickness = 4, CanvasSize = UDim2.new(0, 0, 0, 0), AutomaticCanvasSize = Enum.AutomaticSize.Y,
            Visible = false, ThemeTag = { ScrollBarImageColor3 = "SubText" }, Parent = win.ContentArea
        }, {
            Creator.New("UIListLayout", { SortOrder = Enum.SortOrder.LayoutOrder, Padding = UDim.new(0, 10) }),
            Creator.New("UIPadding", {
                PaddingLeft = UDim.new(0, 18), PaddingRight = UDim.new(0, 18),
                PaddingTop = UDim.new(0, 16), PaddingBottom = UDim.new(0, 24)
            })
        })

        local tabObj = {
            Title = tabTitle,
            Button = tabBtn,
            Container = pageScroll,
            _elementCount = 0
        }

        function tabObj:Activate()
            for _, t in ipairs(win.Tabs) do
                t.Container.Visible = false
                t.Button.BackgroundTransparency = 1
                t.Button.Title.TextColor3 = WindUI.Themes[WindUI.Theme].SubText or Color3.fromRGB(150, 150, 150)
                if t._indMotor then t._indMotor(1) end
                if t._icoLbl then t._icoLbl.ImageColor3 = WindUI.Themes[WindUI.Theme].SubText or Color3.fromRGB(150, 150, 150) end
            end
            win.ActiveTab = self
            self.Container.Visible = true
            setTabBg(0.85)
            titleLbl.TextColor3 = WindUI.Themes[WindUI.Theme].Text or Color3.fromRGB(255, 255, 255)
            setInd(0)
            if icoLbl then icoLbl.ImageColor3 = WindUI.Themes[WindUI.Theme].Accent or Color3.fromRGB(255, 255, 255) end
        end
        tabObj._indMotor = setInd
        tabObj._icoLbl = icoLbl

        tabBtn.MouseButton1Click:Connect(function()
            tabObj:Activate()
        end)

        table.insert(win.Tabs, tabObj)
        if #win.Tabs == 1 then
            tabObj:Activate()
        end

        -- Attach Element Adders directly to tabObj
        function tabObj:AddSection(secTitle, secIcon)
            return WindUI.Elements.AddSection(self, secTitle, secIcon)
        end
        function tabObj:AddParagraph(pCfg) return WindUI.Elements.AddParagraph(self, pCfg) end
        function tabObj:AddButton(bCfg) return WindUI.Elements.AddButton(self, bCfg) end
        function tabObj:AddToggle(idx, tCfg) return WindUI.Elements.AddToggle(self, idx, tCfg) end
        function tabObj:AddSlider(idx, sCfg) return WindUI.Elements.AddSlider(self, idx, sCfg) end
        function tabObj:AddDropdown(idx, dCfg) return WindUI.Elements.AddDropdown(self, idx, dCfg) end
        function tabObj:AddInput(idx, iCfg) return WindUI.Elements.AddInput(self, idx, iCfg) end
        function tabObj:AddColorpicker(idx, cCfg) return WindUI.Elements.AddColorpicker(self, idx, cCfg) end
        function tabObj:AddKeybind(idx, kCfg) return WindUI.Elements.AddKeybind(self, idx, kCfg) end
        function tabObj:AddCodeBlock(cCfg) return WindUI.Elements.AddCodeBlock(self, cCfg) end
        function tabObj:AddProgressBar(pCfg) return WindUI.Elements.AddProgressBar(self, pCfg) end
        function tabObj:AddCircularProgress(cCfg) return WindUI.Elements.AddCircularProgress(self, cCfg) end
        function tabObj:AddStepSlider(idx, sCfg) return WindUI.Elements.AddStepSlider(self, idx, sCfg) end
        function tabObj:AddDatePicker(idx, dCfg) return WindUI.Elements.AddDatePicker(self, idx, dCfg) end
        function tabObj:AddDiscordBanner(dCfg) return WindUI.Elements.AddDiscordBanner(self, dCfg) end
        function tabObj:AddViewport3D(vCfg) return WindUI.Elements.AddViewport3D(self, vCfg) end
        function tabObj:AddDivider() return WindUI.Elements.AddDivider(self) end
        function tabObj:AddSpace(height) return WindUI.Elements.AddSpace(self, height) end

        return tabObj
    end

    WindUI.Window = win
    return win
end

WindUI.CreateWindow = WindowAPI.New
""")
print("Part 8 added.")

# PART 9: Comprehensive UI Elements Implementation
code_parts.append("""
--[[
================================================================================
    All UI Elements & Components Implementation
================================================================================
--]]
local Elements = {}
WindUI.Elements = Elements

local function RegisterElement(parentTab, frame, title)
    parentTab._elementCount = (parentTab._elementCount or 0) + 1
    frame.LayoutOrder = parentTab._elementCount
    if WindUI.Window and WindUI.Window.AllElements then
        WindUI.Window.AllElements[frame] = tostring(title or ""):lower()
    end
end

-- 1. AddSection
function Elements.AddSection(parentTab, secTitle, secIcon)
    local wrap = Creator.New("Frame", {
        Size = UDim2.new(1, 0, 0, 32), BackgroundTransparency = 1, AutomaticSize = Enum.AutomaticSize.Y, Parent = parentTab.Container
    }, { Creator.New("UIListLayout", { SortOrder = Enum.SortOrder.LayoutOrder, Padding = UDim.new(0, 6) }) })

    local head = Creator.New("TextButton", {
        Text = "", Size = UDim2.new(1, 0, 0, 26), BackgroundTransparency = 1, Parent = wrap
    })
    local arrow = Creator.New("ImageLabel", {
        Size = UDim2.fromOffset(14, 14), Position = UDim2.new(1, -16, 0.5, -7), BackgroundTransparency = 1,
        Image = WindUI:GetIcon("lucide-chevron-down").Image or "rbxassetid://10709790948", ThemeTag = { ImageColor3 = "SubText" }, Parent = head
    })
    if secIcon then
        Creator.New("ImageLabel", {
            Size = UDim2.fromOffset(16, 16), Position = UDim2.new(0, 0, 0.5, -8), BackgroundTransparency = 1,
            Image = WindUI:GetIcon(secIcon).Image or "", ThemeTag = { ImageColor3 = "Accent" }, Parent = head
        })
    end
    Creator.New("TextLabel", {
        FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.Bold),
        Text = secTitle, TextSize = 14, Size = UDim2.new(1, -50, 1, 0), Position = UDim2.new(0, secIcon and 24 or 0, 0, 0),
        BackgroundTransparency = 1, TextXAlignment = Enum.TextXAlignment.Left, ThemeTag = { TextColor3 = "Text" }, Parent = head
    })

    local innerContainer = Creator.New("Frame", {
        Size = UDim2.new(1, 0, 0, 0), BackgroundTransparency = 1, AutomaticSize = Enum.AutomaticSize.Y, Parent = wrap
    }, {
        Creator.New("UIListLayout", { SortOrder = Enum.SortOrder.LayoutOrder, Padding = UDim.new(0, 8) }),
        Creator.New("UIPadding", { PaddingLeft = UDim.new(0, 8) })
    })

    local open = true
    head.MouseButton1Click:Connect(function()
        open = not open
        innerContainer.Visible = open
        arrow.Rotation = open and 0 or -90
    end)

    RegisterElement(parentTab, wrap, secTitle)

    local secObj = { Container = innerContainer, _elementCount = 0 }
    function secObj:AddParagraph(pCfg) return Elements.AddParagraph(self, pCfg) end
    function secObj:AddButton(bCfg) return Elements.AddButton(self, bCfg) end
    function secObj:AddToggle(idx, tCfg) return Elements.AddToggle(self, idx, tCfg) end
    function secObj:AddSlider(idx, sCfg) return Elements.AddSlider(self, idx, sCfg) end
    function secObj:AddDropdown(idx, dCfg) return Elements.AddDropdown(self, idx, dCfg) end
    function secObj:AddInput(idx, iCfg) return Elements.AddInput(self, idx, iCfg) end
    function secObj:AddColorpicker(idx, cCfg) return Elements.AddColorpicker(self, idx, cCfg) end
    function secObj:AddKeybind(idx, kCfg) return Elements.AddKeybind(self, idx, kCfg) end
    function secObj:AddCodeBlock(cCfg) return Elements.AddCodeBlock(self, cCfg) end
    function secObj:AddProgressBar(pCfg) return Elements.AddProgressBar(self, pCfg) end
    function secObj:AddCircularProgress(cCfg) return Elements.AddCircularProgress(self, cCfg) end
    function secObj:AddStepSlider(idx, sCfg) return Elements.AddStepSlider(self, idx, sCfg) end
    function secObj:AddDatePicker(idx, dCfg) return Elements.AddDatePicker(self, idx, dCfg) end
    function secObj:AddDiscordBanner(dCfg) return Elements.AddDiscordBanner(self, dCfg) end
    function secObj:AddViewport3D(vCfg) return Elements.AddViewport3D(self, vCfg) end
    function secObj:AddDivider() return Elements.AddDivider(self) end
    function secObj:AddSpace(height) return Elements.AddSpace(self, height) end
    return secObj
end

-- 2. AddParagraph
function Elements.AddParagraph(parentTab, pCfg)
    pCfg = pCfg or {}
    local title = (type(pCfg) == "string" and pCfg) or pCfg.Title or "Paragraph"
    local desc = (type(pCfg) == "table" and pCfg.Desc) or ""

    local wrap = Creator.New("Frame", {
        Size = UDim2.new(1, 0, 0, 0), AutomaticSize = Enum.AutomaticSize.Y, ThemeTag = { BackgroundColor3 = "Element" }, Parent = parentTab.Container
    }, {
        Creator.New("UICorner", { CornerRadius = UDim.new(0, 8) }),
        Creator.New("UIStroke", { Thickness = 1, Transparency = 0.6, ThemeTag = { Color = "ElementBorder" } }),
        Creator.New("UIPadding", { PaddingTop = UDim.new(0, 10), PaddingBottom = UDim.new(0, 10), PaddingLeft = UDim.new(0, 12), PaddingRight = UDim.new(0, 12) }),
        Creator.New("UIListLayout", { SortOrder = Enum.SortOrder.LayoutOrder, Padding = UDim.new(0, 4) })
    })

    local tLbl = Creator.New("TextLabel", {
        FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.SemiBold),
        Text = title, TextSize = 13, Size = UDim2.new(1, 0, 0, 16), BackgroundTransparency = 1, TextXAlignment = Enum.TextXAlignment.Left,
        ThemeTag = { TextColor3 = "Text" }, Parent = wrap
    })
    local dLbl = Creator.New("TextLabel", {
        FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.Regular),
        Text = desc, TextSize = 12, Size = UDim2.new(1, 0, 0, 0), AutomaticSize = Enum.AutomaticSize.Y, BackgroundTransparency = 1,
        TextWrapped = true, TextXAlignment = Enum.TextXAlignment.Left, ThemeTag = { TextColor3 = "SubText" }, Visible = (desc ~= ""), Parent = wrap
    })

    RegisterElement(parentTab, wrap, title)
    return {
        Frame = wrap,
        SetTitle = function(selfP, t) tLbl.Text = t end,
        SetDesc = function(selfP, d) dLbl.Text = d; dLbl.Visible = (d ~= "") end
    }
end

-- 3. AddButton
function Elements.AddButton(parentTab, bCfg)
    bCfg = bCfg or {}
    local title = bCfg.Title or "Button"
    local desc = bCfg.Desc or ""
    local icon = bCfg.Icon
    local callback = bCfg.Callback or function() end

    local btn = Creator.New("TextButton", {
        Text = "", Size = UDim2.new(1, 0, 0, desc ~= "" and 48 or 38), ThemeTag = { BackgroundColor3 = "Element" }, Parent = parentTab.Container
    }, {
        Creator.New("UICorner", { CornerRadius = UDim.new(0, 8) }),
        Creator.New("UIStroke", { Thickness = 1, Transparency = 0.5, ThemeTag = { Color = "ElementBorder" } })
    })
    local bgMotor, setBg = Creator.SpringMotor(1, btn, "BackgroundTransparency")
    setBg(0.1)

    btn.MouseEnter:Connect(function() setBg(0.0) end)
    btn.MouseLeave:Connect(function() setBg(0.1) end)
    btn.MouseButton1Down:Connect(function() setBg(0.3) end)
    btn.MouseButton1Up:Connect(function() setBg(0.0) end)

    local leftOff = 14
    if icon then
        Creator.New("ImageLabel", {
            Size = UDim2.fromOffset(18, 18), Position = UDim2.new(0, 14, 0.5, -9), BackgroundTransparency = 1,
            Image = WindUI:GetIcon(icon).Image or "", ThemeTag = { ImageColor3 = "Accent" }, Parent = btn
        })
        leftOff = 40
    end

    Creator.New("TextLabel", {
        FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.SemiBold),
        Text = title, TextSize = 13, Size = UDim2.new(1, -(leftOff + 10), 0, 16), Position = UDim2.new(0, leftOff, 0, desc ~= "" and 8 or 11),
        BackgroundTransparency = 1, TextXAlignment = Enum.TextXAlignment.Left, ThemeTag = { TextColor3 = "Text" }, Parent = btn
    })
    if desc ~= "" then
        Creator.New("TextLabel", {
            FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.Regular),
            Text = desc, TextSize = 11, Size = UDim2.new(1, -(leftOff + 10), 0, 14), Position = UDim2.new(0, leftOff, 0, 26),
            BackgroundTransparency = 1, TextXAlignment = Enum.TextXAlignment.Left, ThemeTag = { TextColor3 = "SubText" }, Parent = btn
        })
    end

    btn.MouseButton1Click:Connect(function() pcall(callback) end)
    RegisterElement(parentTab, btn, title)
    return { Frame = btn, SetTitle = function(selfB, t) btn.Title.Text = t end }
end

-- 4. AddToggle
function Elements.AddToggle(parentTab, idx, tCfg)
    if type(idx) == "table" then tCfg = idx; idx = tCfg.Idx or tCfg.Title or "Toggle" end
    tCfg = tCfg or {}
    local title = tCfg.Title or "Toggle"
    local desc = tCfg.Desc or ""
    local default = (tCfg.Default == true or tCfg.Value == true)
    local callback = tCfg.Callback or function() end

    local wrap = Creator.New("TextButton", {
        Text = "", Size = UDim2.new(1, 0, 0, desc ~= "" and 48 or 38), ThemeTag = { BackgroundColor3 = "Element" }, Parent = parentTab.Container
    }, {
        Creator.New("UICorner", { CornerRadius = UDim.new(0, 8) }),
        Creator.New("UIStroke", { Thickness = 1, Transparency = 0.5, ThemeTag = { Color = "ElementBorder" } })
    })

    Creator.New("TextLabel", {
        FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.SemiBold),
        Text = title, TextSize = 13, Size = UDim2.new(1, -70, 0, 16), Position = UDim2.new(0, 14, 0, desc ~= "" and 8 or 11),
        BackgroundTransparency = 1, TextXAlignment = Enum.TextXAlignment.Left, ThemeTag = { TextColor3 = "Text" }, Parent = wrap
    })
    if desc ~= "" then
        Creator.New("TextLabel", {
            FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.Regular),
            Text = desc, TextSize = 11, Size = UDim2.new(1, -70, 0, 14), Position = UDim2.new(0, 14, 0, 26),
            BackgroundTransparency = 1, TextXAlignment = Enum.TextXAlignment.Left, ThemeTag = { TextColor3 = "SubText" }, Parent = wrap
        })
    end

    local pill = Creator.New("Frame", {
        Size = UDim2.fromOffset(40, 22), Position = UDim2.new(1, -54, 0.5, -11),
        ThemeTag = { BackgroundColor3 = default and "Accent" or "ToggleSlider" }, Parent = wrap
    }, { Creator.New("UICorner", { CornerRadius = UDim.new(1, 0) }) })

    local dot = Creator.New("Frame", {
        Size = UDim2.fromOffset(16, 16), Position = UDim2.new(0, default and 21 or 3, 0.5, -8),
        ThemeTag = { BackgroundColor3 = "ToggleToggled" }, Parent = pill
    }, { Creator.New("UICorner", { CornerRadius = UDim.new(1, 0) }) })

    local dotMotor, setDotPos = Creator.SpringMotor(default and 21 or 3, dot, "Position")
    setDotPos = function(posOffset)
        dotMotor:SetGoal(Spring.new(posOffset, { frequency = 7, dampingRatio = 0.85 }))
    end

    local toggleObj = { Value = default, Type = "Toggle", Idx = idx, OnChangedSignal = Signal.new() }
    function toggleObj:SetValue(newVal)
        self.Value = (newVal == true)
        pill.BackgroundColor3 = self.Value and (WindUI.Themes[WindUI.Theme].Accent or Color3.fromRGB(0, 150, 255)) or (WindUI.Themes[WindUI.Theme].ToggleSlider or Color3.fromRGB(60, 60, 60))
        setDotPos(self.Value and 21 or 3)
        pcall(callback, self.Value)
        self.OnChangedSignal:Fire(self.Value)
    end
    function toggleObj:OnChanged(fn) return self.OnChangedSignal:Connect(fn) end

    wrap.MouseButton1Click:Connect(function()
        toggleObj:SetValue(not toggleObj.Value)
    end)

    if idx and WindUI.Options then WindUI.Options[idx] = toggleObj end
    RegisterElement(parentTab, wrap, title)
    return toggleObj
end

-- 5. AddSlider
function Elements.AddSlider(parentTab, idx, sCfg)
    if type(idx) == "table" then sCfg = idx; idx = sCfg.Idx or sCfg.Title or "Slider" end
    sCfg = sCfg or {}
    local title = sCfg.Title or "Slider"
    local desc = sCfg.Desc or ""
    local min = sCfg.Min or 0
    local max = sCfg.Max or 100
    local step = sCfg.Step or 1
    local default = sCfg.Default or sCfg.Value or min
    local suffix = sCfg.Suffix or ""
    local callback = sCfg.Callback or function() end

    local wrap = Creator.New("Frame", {
        Size = UDim2.new(1, 0, 0, desc ~= "" and 58 or 48), ThemeTag = { BackgroundColor3 = "Element" }, Parent = parentTab.Container
    }, {
        Creator.New("UICorner", { CornerRadius = UDim.new(0, 8) }),
        Creator.New("UIStroke", { Thickness = 1, Transparency = 0.5, ThemeTag = { Color = "ElementBorder" } })
    })

    Creator.New("TextLabel", {
        FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.SemiBold),
        Text = title, TextSize = 13, Size = UDim2.new(1, -100, 0, 16), Position = UDim2.new(0, 14, 0, 10),
        BackgroundTransparency = 1, TextXAlignment = Enum.TextXAlignment.Left, ThemeTag = { TextColor3 = "Text" }, Parent = wrap
    })

    local valInput = Creator.New("TextBox", {
        FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.Bold),
        Text = tostring(default) .. suffix, TextSize = 12, Size = UDim2.fromOffset(60, 20), Position = UDim2.new(1, -74, 0, 8),
        BackgroundTransparency = 1, TextXAlignment = Enum.TextXAlignment.Right, ThemeTag = { TextColor3 = "Accent" }, Parent = wrap
    })

    local rail = Creator.New("TextButton", {
        Text = "", Size = UDim2.new(1, -28, 0, 6), Position = UDim2.new(0, 14, 1, -16),
        ThemeTag = { BackgroundColor3 = "SliderRail" }, Parent = wrap
    }, { Creator.New("UICorner", { CornerRadius = UDim.new(1, 0) }) })

    local fill = Creator.New("Frame", {
        Size = UDim2.new((default - min) / (max - min), 0, 1, 0), ThemeTag = { BackgroundColor3 = "Accent" }, Parent = rail
    }, { Creator.New("UICorner", { CornerRadius = UDim.new(1, 0) }) })

    local knob = Creator.New("Frame", {
        Size = UDim2.fromOffset(14, 14), Position = UDim2.new(1, -7, 0.5, -7),
        BackgroundColor3 = Color3.fromRGB(255, 255, 255), Parent = fill
    }, { Creator.New("UICorner", { CornerRadius = UDim.new(1, 0) }) })

    local sliderObj = { Value = default, Type = "Slider", Idx = idx, OnChangedSignal = Signal.new() }
    function sliderObj:SetValue(val)
        val = math.clamp(WindUI.Round(val, step < 1 and 2 or 0), min, max)
        self.Value = val
        fill.Size = UDim2.new((val - min) / (max - min), 0, 1, 0)
        valInput.Text = tostring(val) .. suffix
        pcall(callback, val)
        self.OnChangedSignal:Fire(val)
    end
    function sliderObj:OnChanged(fn) return self.OnChangedSignal:Connect(fn) end

    local dragging = false
    rail.InputBegan:Connect(function(inp)
        if inp.UserInputType == Enum.UserInputType.MouseButton1 or inp.UserInputType == Enum.UserInputType.Touch then
            dragging = true
            local percent = math.clamp((inp.Position.X - rail.AbsolutePosition.X) / rail.AbsoluteSize.X, 0, 1)
            sliderObj:SetValue(min + (max - min) * percent)
        end
    end)
    Services.UserInputService.InputEnded:Connect(function(inp)
        if inp.UserInputType == Enum.UserInputType.MouseButton1 or inp.UserInputType == Enum.UserInputType.Touch then
            dragging = false
        end
    end)
    Services.UserInputService.InputChanged:Connect(function(inp)
        if dragging and (inp.UserInputType == Enum.UserInputType.MouseMovement or inp.UserInputType == Enum.UserInputType.Touch) then
            local percent = math.clamp((inp.Position.X - rail.AbsolutePosition.X) / rail.AbsoluteSize.X, 0, 1)
            sliderObj:SetValue(min + (max - min) * percent)
        end
    end)

    valInput.FocusLost:Connect(function()
        local num = tonumber(valInput.Text:gsub("[^%d%.%-]", ""))
        if num then sliderObj:SetValue(num) else sliderObj:SetValue(sliderObj.Value) end
    end)

    if idx and WindUI.Options then WindUI.Options[idx] = sliderObj end
    RegisterElement(parentTab, wrap, title)
    return sliderObj
end

-- 6. AddDropdown (Renders popup outside window layer!)
function Elements.AddDropdown(parentTab, idx, dCfg)
    if type(idx) == "table" then dCfg = idx; idx = dCfg.Idx or dCfg.Title or "Dropdown" end
    dCfg = dCfg or {}
    local title = dCfg.Title or "Dropdown"
    local desc = dCfg.Desc or ""
    local values = dCfg.Values or {}
    local multi = (dCfg.Multi == true)
    local default = dCfg.Default or (multi and {} or (values[1] or nil))
    local callback = dCfg.Callback or function() end

    local wrap = Creator.New("Frame", {
        Size = UDim2.new(1, 0, 0, desc ~= "" and 48 or 38), ThemeTag = { BackgroundColor3 = "Element" }, Parent = parentTab.Container
    }, {
        Creator.New("UICorner", { CornerRadius = UDim.new(0, 8) }),
        Creator.New("UIStroke", { Thickness = 1, Transparency = 0.5, ThemeTag = { Color = "ElementBorder" } })
    })

    Creator.New("TextLabel", {
        FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.SemiBold),
        Text = title, TextSize = 13, Size = UDim2.new(1, -150, 0, 16), Position = UDim2.new(0, 14, 0, desc ~= "" and 8 or 11),
        BackgroundTransparency = 1, TextXAlignment = Enum.TextXAlignment.Left, ThemeTag = { TextColor3 = "Text" }, Parent = wrap
    })

    local selBox = Creator.New("TextButton", {
        Text = "", Size = UDim2.fromOffset(130, 24), Position = UDim2.new(1, -142, 0.5, -12),
        ThemeTag = { BackgroundColor3 = "DropdownFrame" }, Parent = wrap
    }, {
        Creator.New("UICorner", { CornerRadius = UDim.new(0, 6) }),
        Creator.New("UIStroke", { Thickness = 1, Transparency = 0.5, ThemeTag = { Color = "InElementBorder" } })
    })

    local selText = Creator.New("TextLabel", {
        FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.Medium),
        Text = "Select...", TextSize = 12, Size = UDim2.new(1, -26, 1, 0), Position = UDim2.new(0, 8, 0, 0),
        BackgroundTransparency = 1, TextTruncate = Enum.TextTruncate.AtEnd, TextXAlignment = Enum.TextXAlignment.Left,
        ThemeTag = { TextColor3 = "Text" }, Parent = selBox
    })

    Creator.New("ImageLabel", {
        Size = UDim2.fromOffset(12, 12), Position = UDim2.new(1, -18, 0.5, -6), BackgroundTransparency = 1,
        Image = WindUI:GetIcon("lucide-chevron-down").Image or "rbxassetid://10709790948", ThemeTag = { ImageColor3 = "SubText" }, Parent = selBox
    })

    local ddObj = { Value = default, Values = values, Multi = multi, Type = "Dropdown", Idx = idx, OnChangedSignal = Signal.new() }
    
    local function updateText()
        if multi then
            local selectedList = {}
            for k, v in pairs(ddObj.Value) do if v then table.insert(selectedList, k) end end
            selText.Text = #selectedList > 0 and table.concat(selectedList, ", ") or "None"
        else
            selText.Text = tostring(ddObj.Value or "Select...")
        end
    end

    function ddObj:SetValue(val)
        self.Value = val
        updateText()
        pcall(callback, self.Value)
        self.OnChangedSignal:Fire(self.Value)
    end
    function ddObj:SetValues(newVals)
        self.Values = newVals
        self:SetValue(multi and {} or newVals[1])
    end
    function ddObj:OnChanged(fn) return self.OnChangedSignal:Connect(fn) end

    -- Outside Window Popup Modal for Dropdown
    local popupFrame = nil
    selBox.MouseButton1Click:Connect(function()
        if popupFrame and popupFrame.Parent then
            popupFrame:Destroy()
            popupFrame = nil
            return
        end

        local absPos = selBox.AbsolutePosition
        local absSize = selBox.AbsoluteSize
        local popupGui = WindUI.PopupGUI
        if not popupGui then return end

        popupFrame = Creator.New("Frame", {
            Name = "DropdownPopup",
            Size = UDim2.fromOffset(160, math.min(#ddObj.Values * 28 + 36, 220)),
            Position = UDim2.fromOffset(absPos.X + absSize.X - 160, absPos.Y + absSize.Y + 6),
            ThemeTag = { BackgroundColor3 = "DropdownHolder" },
            ZIndex = 100, Parent = popupGui
        }, {
            Creator.New("UICorner", { CornerRadius = UDim.new(0, 8) }),
            Creator.New("UIStroke", { Thickness = 1, ThemeTag = { Color = "Accent" } })
        })

        local scroll = Creator.New("ScrollingFrame", {
            Size = UDim2.new(1, -8, 1, -8), Position = UDim2.new(0, 4, 0, 4), BackgroundTransparency = 1,
            BorderSizePixel = 0, ScrollBarThickness = 3, CanvasSize = UDim2.new(0, 0, 0, 0), AutomaticCanvasSize = Enum.AutomaticSize.Y,
            ThemeTag = { ScrollBarImageColor3 = "SubText" }, Parent = popupFrame
        }, { Creator.New("UIListLayout", { SortOrder = Enum.SortOrder.LayoutOrder, Padding = UDim.new(0, 2) }) })

        for _, opt in ipairs(ddObj.Values) do
            local isSel = multi and (ddObj.Value[opt] == true) or (ddObj.Value == opt)
            local optBtn = Creator.New("TextButton", {
                Text = "", Size = UDim2.new(1, 0, 0, 26),
                ThemeTag = { BackgroundColor3 = isSel and "Accent" or "Element" }, Parent = scroll
            }, {
                Creator.New("UICorner", { CornerRadius = UDim.new(0, 6) }),
                Creator.New("TextLabel", {
                    FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.Medium),
                    Text = tostring(opt), TextSize = 12, Size = UDim2.new(1, -12, 1, 0), Position = UDim2.new(0, 8, 0, 0),
                    BackgroundTransparency = 1, TextXAlignment = Enum.TextXAlignment.Left,
                    ThemeTag = { TextColor3 = isSel and "ToggleToggled" or "Text" }
                })
            })
            optBtn.MouseButton1Click:Connect(function()
                if multi then
                    ddObj.Value[opt] = not ddObj.Value[opt]
                    ddObj:SetValue(ddObj.Value)
                    if popupFrame and popupFrame.Parent then popupFrame:Destroy() popupFrame = nil end
                else
                    ddObj:SetValue(opt)
                    if popupFrame and popupFrame.Parent then popupFrame:Destroy() popupFrame = nil end
                end
            end)
        end

        local closeConn
        closeConn = Services.UserInputService.InputBegan:Connect(function(inp)
            if inp.UserInputType == Enum.UserInputType.MouseButton1 or inp.UserInputType == Enum.UserInputType.Touch then
                local mp = inp.Position
                local fp, fs = popupFrame.AbsolutePosition, popupFrame.AbsoluteSize
                if mp.X < fp.X or mp.X > fp.X + fs.X or mp.Y < fp.Y or mp.Y > fp.Y + fs.Y then
                    pcall(function() closeConn:Disconnect() end)
                    if popupFrame and popupFrame.Parent then popupFrame:Destroy() popupFrame = nil end
                end
            end
        end)
    end)

    updateText()
    if idx and WindUI.Options then WindUI.Options[idx] = ddObj end
    RegisterElement(parentTab, wrap, title)
    return ddObj
end

-- 7. AddInput / Textbox
function Elements.AddInput(parentTab, idx, iCfg)
    if type(idx) == "table" then iCfg = idx; idx = iCfg.Idx or iCfg.Title or "Input" end
    iCfg = iCfg or {}
    local title = iCfg.Title or "Input"
    local desc = iCfg.Desc or ""
    local placeholder = iCfg.Placeholder or "Type here..."
    local default = iCfg.Default or iCfg.Value or ""
    local numeric = iCfg.Numeric or false
    local callback = iCfg.Callback or function() end

    local wrap = Creator.New("Frame", {
        Size = UDim2.new(1, 0, 0, desc ~= "" and 48 or 38), ThemeTag = { BackgroundColor3 = "Element" }, Parent = parentTab.Container
    }, {
        Creator.New("UICorner", { CornerRadius = UDim.new(0, 8) }),
        Creator.New("UIStroke", { Thickness = 1, Transparency = 0.5, ThemeTag = { Color = "ElementBorder" } })
    })

    Creator.New("TextLabel", {
        FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.SemiBold),
        Text = title, TextSize = 13, Size = UDim2.new(1, -160, 0, 16), Position = UDim2.new(0, 14, 0, desc ~= "" and 8 or 11),
        BackgroundTransparency = 1, TextXAlignment = Enum.TextXAlignment.Left, ThemeTag = { TextColor3 = "Text" }, Parent = wrap
    })

    local inputWrap = Creator.New("Frame", {
        Size = UDim2.fromOffset(140, 24), Position = UDim2.new(1, -150, 0.5, -12),
        ThemeTag = { BackgroundColor3 = "Input" }, Parent = wrap
    }, {
        Creator.New("UICorner", { CornerRadius = UDim.new(0, 6) }),
        Creator.New("UIStroke", { Thickness = 1, Transparency = 0.5, ThemeTag = { Color = "InElementBorder" } })
    })

    local tb = Creator.New("TextBox", {
        FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.Medium),
        PlaceholderText = placeholder, Text = default, TextSize = 12, Size = UDim2.new(1, -16, 1, 0), Position = UDim2.new(0, 8, 0, 0),
        BackgroundTransparency = 1, ClearTextOnFocus = false, TextXAlignment = Enum.TextXAlignment.Left,
        ThemeTag = { TextColor3 = "Text", PlaceholderColor3 = "SubText" }, Parent = inputWrap
    })

    local inpObj = { Value = default, Type = "Input", Idx = idx, OnChangedSignal = Signal.new() }
    function inpObj:SetValue(newVal)
        self.Value = tostring(newVal)
        tb.Text = self.Value
        pcall(callback, self.Value)
        self.OnChangedSignal:Fire(self.Value)
    end
    function inpObj:OnChanged(fn) return self.OnChangedSignal:Connect(fn) end

    tb.FocusLost:Connect(function()
        local txt = tb.Text
        if numeric then txt = txt:gsub("[^%d%.%-]", "") tb.Text = txt end
        inpObj:SetValue(txt)
    end)

    if idx and WindUI.Options then WindUI.Options[idx] = inpObj end
    RegisterElement(parentTab, wrap, title)
    return inpObj
end

-- 8. AddColorpicker
function Elements.AddColorpicker(parentTab, idx, cCfg)
    if type(idx) == "table" then cCfg = idx; idx = cCfg.Idx or cCfg.Title or "Colorpicker" end
    cCfg = cCfg or {}
    local title = cCfg.Title or "Colorpicker"
    local desc = cCfg.Desc or ""
    local default = cCfg.Default or cCfg.Color or Color3.fromRGB(255, 255, 255)
    local transparency = cCfg.Transparency or 0
    local callback = cCfg.Callback or function() end

    local wrap = Creator.New("Frame", {
        Size = UDim2.new(1, 0, 0, desc ~= "" and 48 or 38), ThemeTag = { BackgroundColor3 = "Element" }, Parent = parentTab.Container
    }, {
        Creator.New("UICorner", { CornerRadius = UDim.new(0, 8) }),
        Creator.New("UIStroke", { Thickness = 1, Transparency = 0.5, ThemeTag = { Color = "ElementBorder" } })
    })

    Creator.New("TextLabel", {
        FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.SemiBold),
        Text = title, TextSize = 13, Size = UDim2.new(1, -70, 0, 16), Position = UDim2.new(0, 14, 0, desc ~= "" and 8 or 11),
        BackgroundTransparency = 1, TextXAlignment = Enum.TextXAlignment.Left, ThemeTag = { TextColor3 = "Text" }, Parent = wrap
    })

    local chip = Creator.New("TextButton", {
        Text = "", Size = UDim2.fromOffset(36, 20), Position = UDim2.new(1, -48, 0.5, -10),
        BackgroundColor3 = default, Parent = wrap
    }, {
        Creator.New("UICorner", { CornerRadius = UDim.new(0, 6) }),
        Creator.New("UIStroke", { Thickness = 1, ThemeTag = { Color = "InElementBorder" } })
    })

    local cpObj = { Value = default, Transparency = transparency, Type = "Colorpicker", Idx = idx, OnChangedSignal = Signal.new() }
    function cpObj:SetValue(col, trans)
        self.Value = col or self.Value
        self.Transparency = trans or self.Transparency
        chip.BackgroundColor3 = self.Value
        pcall(callback, self.Value, self.Transparency)
        self.OnChangedSignal:Fire(self.Value, self.Transparency)
    end
    function cpObj:SetValueRGB(col, trans) self:SetValue(col, trans) end
    function cpObj:OnChanged(fn) return self.OnChangedSignal:Connect(fn) end

    chip.MouseButton1Click:Connect(function()
        -- Simple color cycling/picker popup simulation
        local h, s, v = cpObj.Value:ToHSV()
        h = (h + 0.15) % 1
        cpObj:SetValue(Color3.fromHSV(h, 1, 1), cpObj.Transparency)
    end)

    if idx and WindUI.Options then WindUI.Options[idx] = cpObj end
    RegisterElement(parentTab, wrap, title)
    return cpObj
end

-- 9. AddKeybind
function Elements.AddKeybind(parentTab, idx, kCfg)
    if type(idx) == "table" then kCfg = idx; idx = kCfg.Idx or kCfg.Title or "Keybind" end
    kCfg = kCfg or {}
    local title = kCfg.Title or "Keybind"
    local desc = kCfg.Desc or ""
    local defaultKey = kCfg.Default or kCfg.Value or Enum.KeyCode.E
    local mode = kCfg.Mode or "Toggle" -- Toggle, Hold, Always
    local callback = kCfg.Callback or function() end

    local wrap = Creator.New("Frame", {
        Size = UDim2.new(1, 0, 0, desc ~= "" and 48 or 38), ThemeTag = { BackgroundColor3 = "Element" }, Parent = parentTab.Container
    }, {
        Creator.New("UICorner", { CornerRadius = UDim.new(0, 8) }),
        Creator.New("UIStroke", { Thickness = 1, Transparency = 0.5, ThemeTag = { Color = "ElementBorder" } })
    })

    Creator.New("TextLabel", {
        FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.SemiBold),
        Text = title, TextSize = 13, Size = UDim2.new(1, -100, 0, 16), Position = UDim2.new(0, 14, 0, desc ~= "" and 8 or 11),
        BackgroundTransparency = 1, TextXAlignment = Enum.TextXAlignment.Left, ThemeTag = { TextColor3 = "Text" }, Parent = wrap
    })

    local kbBtn = Creator.New("TextButton", {
        Text = tostring(defaultKey.Name or defaultKey), FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.Bold),
        TextSize = 11, Size = UDim2.fromOffset(70, 22), Position = UDim2.new(1, -82, 0.5, -11),
        ThemeTag = { BackgroundColor3 = "Keybind", TextColor3 = "Accent" }, Parent = wrap
    }, {
        Creator.New("UICorner", { CornerRadius = UDim.new(0, 6) }),
        Creator.New("UIStroke", { Thickness = 1, Transparency = 0.5, ThemeTag = { Color = "InElementBorder" } })
    })

    local kbObj = { Value = defaultKey, Mode = mode, Type = "Keybind", Idx = idx, OnChangedSignal = Signal.new() }
    function kbObj:SetValue(key, m)
        if typeof(key) == "string" and Enum.KeyCode[key] then key = Enum.KeyCode[key] end
        self.Value = key or self.Value
        self.Mode = m or self.Mode
        kbBtn.Text = tostring(self.Value.Name or self.Value)
        self.OnChangedSignal:Fire(self.Value, self.Mode)
    end
    function kbObj:OnChanged(fn) return self.OnChangedSignal:Connect(fn) end

    local listening = false
    kbBtn.MouseButton1Click:Connect(function()
        listening = true
        kbBtn.Text = "..."
    end)

    Services.UserInputService.InputBegan:Connect(function(inp, gpe)
        if listening and inp.UserInputType == Enum.UserInputType.Keyboard then
            listening = false
            kbObj:SetValue(inp.KeyCode, kbObj.Mode)
        elseif not gpe and inp.KeyCode == kbObj.Value then
            pcall(callback, kbObj.Mode == "Toggle")
        end
    end)

    if idx and WindUI.Options then WindUI.Options[idx] = kbObj end
    RegisterElement(parentTab, wrap, title)
    return kbObj
end

-- 10. AddCodeBlock
function Elements.AddCodeBlock(parentTab, cCfg)
    cCfg = cCfg or {}
    local title = cCfg.Title or "Code Snippet"
    local codeText = cCfg.Code or cCfg.Text or "print('Hello WindUI Ultimate!')"

    local wrap = Creator.New("Frame", {
        Size = UDim2.new(1, 0, 0, 130), ThemeTag = { BackgroundColor3 = "Element" }, Parent = parentTab.Container
    }, {
        Creator.New("UICorner", { CornerRadius = UDim.new(0, 8) }),
        Creator.New("UIStroke", { Thickness = 1, Transparency = 0.5, ThemeTag = { Color = "ElementBorder" } })
    })

    Creator.New("TextLabel", {
        FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.Bold),
        Text = title, TextSize = 13, Size = UDim2.new(1, -70, 0, 24), Position = UDim2.new(0, 14, 0, 6),
        BackgroundTransparency = 1, TextXAlignment = Enum.TextXAlignment.Left, ThemeTag = { TextColor3 = "Text" }, Parent = wrap
    })

    local copyBtn = Creator.New("TextButton", {
        Text = "Copy", FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.SemiBold),
        TextSize = 11, Size = UDim2.fromOffset(50, 22), Position = UDim2.new(1, -62, 0, 6),
        ThemeTag = { BackgroundColor3 = "Accent", TextColor3 = "ToggleToggled" }, Parent = wrap
    }, { Creator.New("UICorner", { CornerRadius = UDim.new(0, 6) }) })

    copyBtn.MouseButton1Click:Connect(function()
        if setclipboard then setclipboard(codeText) end
        copyBtn.Text = "Copied!"
        task.delay(1.5, function() copyBtn.Text = "Copy" end)
    end)

    local boxScroll = Creator.New("ScrollingFrame", {
        Size = UDim2.new(1, -24, 1, -40), Position = UDim2.new(0, 12, 0, 32),
        ThemeTag = { BackgroundColor3 = "Input" }, BorderSizePixel = 0, ScrollBarThickness = 3,
        CanvasSize = UDim2.new(0, 0, 0, 0), AutomaticCanvasSize = Enum.AutomaticSize.XY, Parent = wrap
    }, {
        Creator.New("UICorner", { CornerRadius = UDim.new(0, 6) }),
        Creator.New("UIPadding", { PaddingTop = UDim.new(0, 6), PaddingLeft = UDim.new(0, 8) })
    })

    Creator.New("TextLabel", {
        FontFace = Font.new("rbxasset://fonts/families/RobotoMono.json", Enum.FontWeight.Regular),
        Text = codeText, TextSize = 12, Size = UDim2.new(1, 0, 0, 0), AutomaticSize = Enum.AutomaticSize.XY,
        BackgroundTransparency = 1, TextXAlignment = Enum.TextXAlignment.Left, TextYAlignment = Enum.TextYAlignment.Top,
        ThemeTag = { TextColor3 = "Text" }, Parent = boxScroll
    })

    RegisterElement(parentTab, wrap, title)
    return { Frame = wrap }
end

-- 11. AddProgressBar & AddCircularProgress
function Elements.AddProgressBar(parentTab, pCfg)
    pCfg = pCfg or {}
    local title = pCfg.Title or "Progress"
    local value = pCfg.Value or 0 -- 0 to 100

    local wrap = Creator.New("Frame", {
        Size = UDim2.new(1, 0, 0, 48), ThemeTag = { BackgroundColor3 = "Element" }, Parent = parentTab.Container
    }, {
        Creator.New("UICorner", { CornerRadius = UDim.new(0, 8) }),
        Creator.New("UIStroke", { Thickness = 1, Transparency = 0.5, ThemeTag = { Color = "ElementBorder" } })
    })

    Creator.New("TextLabel", {
        FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.SemiBold),
        Text = title, TextSize = 13, Size = UDim2.new(1, -60, 0, 16), Position = UDim2.new(0, 14, 0, 8),
        BackgroundTransparency = 1, TextXAlignment = Enum.TextXAlignment.Left, ThemeTag = { TextColor3 = "Text" }, Parent = wrap
    })

    local percentLbl = Creator.New("TextLabel", {
        FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.Bold),
        Text = tostring(value) .. "%", TextSize = 12, Size = UDim2.fromOffset(40, 16), Position = UDim2.new(1, -50, 0, 8),
        BackgroundTransparency = 1, TextXAlignment = Enum.TextXAlignment.Right, ThemeTag = { TextColor3 = "Accent" }, Parent = wrap
    })

    local rail = Creator.New("Frame", {
        Size = UDim2.new(1, -28, 0, 8), Position = UDim2.new(0, 14, 0, 30),
        ThemeTag = { BackgroundColor3 = "SliderRail" }, Parent = wrap
    }, { Creator.New("UICorner", { CornerRadius = UDim.new(1, 0) }) })

    local fill = Creator.New("Frame", {
        Size = UDim2.new(value / 100, 0, 1, 0), ThemeTag = { BackgroundColor3 = "Accent" }, Parent = rail
    }, { Creator.New("UICorner", { CornerRadius = UDim.new(1, 0) }) })

    RegisterElement(parentTab, wrap, title)
    return {
        Frame = wrap,
        SetValue = function(selfP, val)
            val = math.clamp(val, 0, 100)
            fill.Size = UDim2.new(val / 100, 0, 1, 0)
            percentLbl.Text = tostring(val) .. "%"
        end
    }
end

function Elements.AddCircularProgress(parentTab, cCfg)
    cCfg = cCfg or {}
    local title = cCfg.Title or "Loading"
    local wrap = Creator.New("Frame", {
        Size = UDim2.new(1, 0, 0, 48), ThemeTag = { BackgroundColor3 = "Element" }, Parent = parentTab.Container
    }, {
        Creator.New("UICorner", { CornerRadius = UDim.new(0, 8) }),
        Creator.New("UIStroke", { Thickness = 1, Transparency = 0.5, ThemeTag = { Color = "ElementBorder" } })
    })
    Creator.New("TextLabel", {
        FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.SemiBold),
        Text = title, TextSize = 13, Size = UDim2.new(1, -60, 1, 0), Position = UDim2.new(0, 14, 0, 0),
        BackgroundTransparency = 1, TextXAlignment = Enum.TextXAlignment.Left, ThemeTag = { TextColor3 = "Text" }, Parent = wrap
    })
    local spinIco = Creator.New("ImageLabel", {
        Size = UDim2.fromOffset(22, 22), Position = UDim2.new(1, -36, 0.5, -11), BackgroundTransparency = 1,
        Image = WindUI:GetIcon("solar/restart-bold").Image or "rbxassetid://10723434070",
        ThemeTag = { ImageColor3 = "Accent" }, Parent = wrap
    })
    Services.RunService.RenderStepped:Connect(function(dt)
        if spinIco and spinIco.Parent then spinIco.Rotation = (spinIco.Rotation + dt * 180) % 360 end
    end)
    RegisterElement(parentTab, wrap, title)
    return { Frame = wrap }
end

-- 12. AddStepSlider & AddDatePicker & AddDiscordBanner & AddViewport3D & AddDivider & AddSpace
function Elements.AddStepSlider(parentTab, idx, sCfg)
    if type(idx) == "table" then sCfg = idx; idx = sCfg.Idx or sCfg.Title or "StepSlider" end
    sCfg = sCfg or {}
    local title = sCfg.Title or "Select Step"
    local steps = sCfg.Steps or { "Low", "Medium", "High" }
    local default = sCfg.Default or steps[1]
    local callback = sCfg.Callback or function() end

    local wrap = Creator.New("Frame", {
        Size = UDim2.new(1, 0, 0, 60), ThemeTag = { BackgroundColor3 = "Element" }, Parent = parentTab.Container
    }, {
        Creator.New("UICorner", { CornerRadius = UDim.new(0, 8) }),
        Creator.New("UIStroke", { Thickness = 1, Transparency = 0.5, ThemeTag = { Color = "ElementBorder" } })
    })
    Creator.New("TextLabel", {
        FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.SemiBold),
        Text = title, TextSize = 13, Size = UDim2.new(1, -20, 0, 18), Position = UDim2.new(0, 14, 0, 6),
        BackgroundTransparency = 1, TextXAlignment = Enum.TextXAlignment.Left, ThemeTag = { TextColor3 = "Text" }, Parent = wrap
    })

    local stepHolder = Creator.New("Frame", {
        Size = UDim2.new(1, -28, 0, 26), Position = UDim2.new(0, 14, 0, 28), BackgroundTransparency = 1, Parent = wrap
    }, { Creator.New("UIListLayout", { FillDirection = Enum.FillDirection.Horizontal, Padding = UDim.new(0, 6) }) })

    local stObj = { Value = default, Type = "StepSlider", Idx = idx, OnChangedSignal = Signal.new() }
    function stObj:SetValue(v)
        self.Value = v
        for _, btn in ipairs(stepHolder:GetChildren()) do
            if btn:IsA("TextButton") then
                local sel = (btn.Text == v)
                btn.BackgroundColor3 = sel and (WindUI.Themes[WindUI.Theme].Accent or Color3.fromRGB(0, 150, 255)) or (WindUI.Themes[WindUI.Theme].Input or Color3.fromRGB(30, 30, 30))
                btn.TextColor3 = sel and (WindUI.Themes[WindUI.Theme].ToggleToggled or Color3.fromRGB(255, 255, 255)) or (WindUI.Themes[WindUI.Theme].Text or Color3.fromRGB(200, 200, 200))
            end
        end
        pcall(callback, v)
        self.OnChangedSignal:Fire(v)
    end
    function stObj:OnChanged(fn) return self.OnChangedSignal:Connect(fn) end

    local c = #steps
    for _, stepName in ipairs(steps) do
        local btn = Creator.New("TextButton", {
            Text = stepName, FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.Medium),
            TextSize = 11, Size = UDim2.new(1 / c, -((c - 1) * 6 / c), 1, 0), ThemeTag = { BackgroundColor3 = "Input", TextColor3 = "Text" },
            Parent = stepHolder
        }, { Creator.New("UICorner", { CornerRadius = UDim.new(0, 6) }) })
        btn.MouseButton1Click:Connect(function() stObj:SetValue(stepName) end)
    end

    stObj:SetValue(default)
    if idx and WindUI.Options then WindUI.Options[idx] = stObj end
    RegisterElement(parentTab, wrap, title)
    return stObj
end

function Elements.AddDatePicker(parentTab, idx, dCfg)
    if type(idx) == "table" then dCfg = idx; idx = dCfg.Idx or dCfg.Title or "DatePicker" end
    dCfg = dCfg or {}
    local title = dCfg.Title or "Select Date"
    return Elements.AddInput(parentTab, idx, { Title = title, Default = "2026-07-13", Placeholder = "YYYY-MM-DD" })
end

function Elements.AddDiscordBanner(parentTab, dCfg)
    dCfg = dCfg or {}
    local inviteCode = dCfg.InviteCode or dCfg.Invite or "windui"
    local title = dCfg.Title or "Join Our Discord"
    local wrap = Creator.New("Frame", {
        Size = UDim2.new(1, 0, 0, 78), ThemeTag = { BackgroundColor3 = "Element" }, Parent = parentTab.Container
    }, {
        Creator.New("UICorner", { CornerRadius = UDim.new(0, 10) }),
        Creator.New("UIStroke", { Thickness = 1, Transparency = 0.5, ThemeTag = { Color = "ElementBorder" } })
    })
    local icoBg = Creator.New("Frame", {
        Size = UDim2.fromOffset(48, 48), Position = UDim2.new(0, 14, 0.5, -24), BackgroundColor3 = Color3.fromRGB(88, 101, 242), Parent = wrap
    }, { Creator.New("UICorner", { CornerRadius = UDim.new(0, 10) }) })
    Creator.New("TextLabel", {
        FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.Bold),
        Text = "W", TextSize = 24, TextColor3 = Color3.fromRGB(255, 255, 255), Size = UDim2.fromScale(1, 1), BackgroundTransparency = 1, Parent = icoBg
    })
    Creator.New("TextLabel", {
        FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.Bold),
        Text = title, TextSize = 14, Size = UDim2.new(1, -150, 0, 18), Position = UDim2.new(0, 72, 0, 16),
        BackgroundTransparency = 1, TextXAlignment = Enum.TextXAlignment.Left, ThemeTag = { TextColor3 = "Text" }, Parent = wrap
    })
    Creator.New("TextLabel", {
        FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.Medium),
        Text = "discord.gg/" .. inviteCode, TextSize = 12, Size = UDim2.new(1, -150, 0, 16), Position = UDim2.new(0, 72, 0, 38),
        BackgroundTransparency = 1, TextXAlignment = Enum.TextXAlignment.Left, ThemeTag = { TextColor3 = "SubText" }, Parent = wrap
    })
    local joinBtn = Creator.New("TextButton", {
        Text = "Join", FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.Bold),
        TextSize = 12, Size = UDim2.fromOffset(60, 30), Position = UDim2.new(1, -74, 0.5, -15),
        BackgroundColor3 = Color3.fromRGB(88, 101, 242), TextColor3 = Color3.fromRGB(255, 255, 255), Parent = wrap
    }, { Creator.New("UICorner", { CornerRadius = UDim.new(0, 8) }) })
    joinBtn.MouseButton1Click:Connect(function()
        if setclipboard then setclipboard("https://discord.gg/" .. inviteCode) end
        joinBtn.Text = "Copied!"
        task.delay(1.5, function() joinBtn.Text = "Join" end)
    end)
    RegisterElement(parentTab, wrap, title)
    return { Frame = wrap }
end

function Elements.AddViewport3D(parentTab, vCfg)
    vCfg = vCfg or {}
    local title = vCfg.Title or "3D Viewport Preview"
    local obj = vCfg.Object or Instance.new("Part")
    local wrap = Creator.New("Frame", {
        Size = UDim2.new(1, 0, 0, 180), ThemeTag = { BackgroundColor3 = "Element" }, Parent = parentTab.Container
    }, {
        Creator.New("UICorner", { CornerRadius = UDim.new(0, 8) }),
        Creator.New("UIStroke", { Thickness = 1, Transparency = 0.5, ThemeTag = { Color = "ElementBorder" } })
    })
    Creator.New("TextLabel", {
        FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.Bold),
        Text = title, TextSize = 13, Size = UDim2.new(1, -24, 0, 24), Position = UDim2.new(0, 14, 0, 6),
        BackgroundTransparency = 1, TextXAlignment = Enum.TextXAlignment.Left, ThemeTag = { TextColor3 = "Text" }, Parent = wrap
    })
    local vp = Creator.New("ViewportFrame", {
        Size = UDim2.new(1, -24, 1, -42), Position = UDim2.new(0, 12, 0, 34),
        BackgroundTransparency = 0.5, ThemeTag = { BackgroundColor3 = "Input" }, Parent = wrap
    }, { Creator.New("UICorner", { CornerRadius = UDim.new(0, 6) }) })
    local cam = Instance.new("Camera")
    cam.Parent = vp
    vp.CurrentCamera = cam
    if obj then obj.Parent = vp cam.CFrame = CFrame.new(Vector3.new(0, 2, 5), obj:GetPivot().Position) end
    RegisterElement(parentTab, wrap, title)
    return { Frame = wrap, Viewport = vp }
end

function Elements.AddDivider(parentTab)
    local wrap = Creator.New("Frame", {
        Size = UDim2.new(1, 0, 0, 12), BackgroundTransparency = 1, Parent = parentTab.Container
    }, {
        Creator.New("Frame", {
            Size = UDim2.new(1, 0, 0, 1), Position = UDim2.new(0, 0, 0.5, 0), BorderSizePixel = 0,
            ThemeTag = { BackgroundColor3 = "TitleBarLine" }
        })
    })
    RegisterElement(parentTab, wrap, "Divider")
    return { Frame = wrap }
end

function Elements.AddSpace(parentTab, height)
    local wrap = Creator.New("Frame", {
        Size = UDim2.new(1, 0, 0, height or 12), BackgroundTransparency = 1, Parent = parentTab.Container
    })
    RegisterElement(parentTab, wrap, "Space")
    return { Frame = wrap }
end
""")
print("Part 9 added.")

# PART 10: Managers & Export
code_parts.append("""
--[[
================================================================================
    SaveManager Module
================================================================================
--]]
local SaveManager = {
    Folder = "WindSettings",
    Ignore = {},
    Parser = {
        Toggle = { Save = function(o) return { type = "Toggle", val = o.Value } end, Load = function(o, d) if o then o:SetValue(d.val) end end },
        Slider = { Save = function(o) return { type = "Slider", val = o.Value } end, Load = function(o, d) if o then o:SetValue(d.val) end end },
        Dropdown = { Save = function(o) return { type = "Dropdown", val = o.Value } end, Load = function(o, d) if o then o:SetValue(d.val) end end },
        Colorpicker = { Save = function(o) return { type = "Colorpicker", val = o.Value:ToHex(), trans = o.Transparency } end, Load = function(o, d) if o then o:SetValueRGB(Color3.fromHex(d.val), d.trans) end end },
        Keybind = { Save = function(o) return { type = "Keybind", val = o.Value.Name, mode = o.Mode } end, Load = function(o, d) if o then o:SetValue(Enum.KeyCode[d.val] or d.val, d.mode) end end },
        Input = { Save = function(o) return { type = "Input", val = o.Value } end, Load = function(o, d) if o then o:SetValue(d.val) end end }
    }
}

function SaveManager:SetFolder(folderName)
    self.Folder = folderName
    pcall(function()
        if makefolder and not isfolder(self.Folder) then makefolder(self.Folder) end
        if makefolder and not isfolder(self.Folder .. "/configs") then makefolder(self.Folder .. "/configs") end
    end)
end

function SaveManager:SetIgnoreIndexes(list)
    for _, k in ipairs(list) do self.Ignore[k] = true end
end

function SaveManager:Save(configName)
    if not configName or configName == "" then return false, "No config name" end
    local data = { objects = {} }
    for idx, opt in pairs(WindUI.Options) do
        if self.Parser[opt.Type] and not self.Ignore[idx] then
            data.objects[idx] = self.Parser[opt.Type].Save(opt)
        end
    end
    local ok, enc = pcall(Services.HttpService.JSONEncode, Services.HttpService, data)
    if not ok then return false, "Encode failed" end
    pcall(function()
        if writefile then writefile(self.Folder .. "/configs/" .. configName .. ".json", enc) end
    end)
    return true
end

function SaveManager:Load(configName)
    if not configName or configName == "" then return false, "No config name" end
    local path = self.Folder .. "/configs/" .. configName .. ".json"
    local ok, dec = pcall(function()
        if isfile and isfile(path) then
            return Services.HttpService:JSONDecode(readfile(path))
        end
    end)
    if not ok or not dec or not dec.objects then return false, "Invalid file" end
    for idx, savedOpt in pairs(dec.objects) do
        local opt = WindUI.Options[idx]
        if opt and self.Parser[savedOpt.type] then
            task.spawn(function() self.Parser[savedOpt.type].Load(opt, savedOpt) end)
        end
    end
    return true
end

function SaveManager:RefreshConfigList()
    local list = {}
    pcall(function()
        if listfiles then
            for _, f in ipairs(listfiles(self.Folder .. "/configs")) do
                if f:sub(-5) == ".json" then
                    local nm = f:match("([^/\\]+)%.json$")
                    if nm then table.insert(list, nm) end
                end
            end
        end
    end)
    return list
end

function SaveManager:BuildConfigSection(tab)
    self:SetFolder(self.Folder)
    local sec = tab:AddSection("SaveManager Configs", "lucide-folder")
    local nameInp = sec:AddInput("SaveManager_ConfigName", { Title = "Config Name", Placeholder = "Enter config name..." })
    local listDd = sec:AddDropdown("SaveManager_ConfigList", { Title = "Available Configs", Values = self:RefreshConfigList() })
    
    sec:AddButton({ Title = "Create / Overwrite Config", Icon = "solar/diskette-bold", Callback = function()
        local nm = nameInp.Value
        if not nm or nm == "" then nm = listDd.Value end
        if not nm or nm == "" then return WindUI:Notify({ Title = "SaveManager", Content = "Please enter a valid config name.", Type = "Warning", Duration = 3 }) end
        local ok, err = self:Save(nm)
        if ok then
            WindUI:Notify({ Title = "SaveManager", Content = "Successfully saved config: " .. nm, Type = "Success", Duration = 3 })
            listDd:SetValues(self:RefreshConfigList())
        else
            WindUI:Notify({ Title = "SaveManager", Content = "Failed to save: " .. tostring(err), Type = "Error", Duration = 3 })
        end
    end })

    sec:AddButton({ Title = "Load Config", Icon = "solar/upload-minimalistic-bold", Callback = function()
        local nm = listDd.Value
        if not nm or nm == "" then return WindUI:Notify({ Title = "SaveManager", Content = "Please select a config from the list.", Type = "Warning", Duration = 3 }) end
        local ok, err = self:Load(nm)
        if ok then
            WindUI:Notify({ Title = "SaveManager", Content = "Loaded config: " .. nm, Type = "Success", Duration = 3 })
        else
            WindUI:Notify({ Title = "SaveManager", Content = "Failed to load: " .. tostring(err), Type = "Error", Duration = 3 })
        end
    end })

    sec:AddButton({ Title = "Refresh Config List", Icon = "solar/restart-bold", Callback = function()
        listDd:SetValues(self:RefreshConfigList())
        WindUI:Notify({ Title = "SaveManager", Content = "Config list refreshed.", Type = "Info", Duration = 2 })
    end })

    self:SetIgnoreIndexes({ "SaveManager_ConfigName", "SaveManager_ConfigList" })
end

WindUI.SaveManager = SaveManager

--[[
================================================================================
    InterfaceManager Module
================================================================================
--]]
local InterfaceManager = {
    Folder = "WindSettings",
    Settings = { Theme = "Blood Red", Acrylic = true, Transparency = true, Animated = true, MinimizeKey = "LeftControl" }
}

function InterfaceManager:BuildInterfaceSection(tab)
    local sec = tab:AddSection("Interface Settings", "lucide-settings")
    
    sec:AddDropdown("InterfaceTheme", {
        Title = "Theme Selector", Desc = "Switch between 23+ sleek WindUI & Fluent themes live.",
        Values = WindUI.ThemeNames, Default = WindUI.Theme,
        Callback = function(val)
            WindUI:SetTheme(val)
        end
    })

    sec:AddToggle("AnimationToggle", {
        Title = "Animated Theme Shine", Desc = "Dynamic animated gradient sweeps across window borders.",
        Default = WindUI.ShineEnabled,
        Callback = function(val)
            WindUI.ShineEnabled = val
            if WindUI.Window and WindUI.Window.Root then
                Animation.Apply(WindUI.Theme, WindUI.Window.Root)
            end
        end
    })

    sec:AddKeybind("InterfaceMinimizeKey", {
        Title = "Minimize / Restore Keybind", Desc = "Press to instantly toggle minimize floating pill.",
        Default = WindUI.MinimizeKey,
        Callback = function() end
    }):OnChanged(function(newKey)
        WindUI.MinimizeKey = newKey
    end)
end

WindUI.InterfaceManager = InterfaceManager

--[[
================================================================================
    FloatingButtonManager Module
================================================================================
--]]
local FloatingButtonManager = {
    Buttons = {}
}

function FloatingButtonManager:AddButton(id, frame, locked, isCircle)
    self.Buttons[id] = { Frame = frame, Locked = locked, IsCircle = isCircle }
end

WindUI.FloatingButtonManager = FloatingButtonManager

--[[
================================================================================
    MediaManager Module
================================================================================
--]]
local MediaManager = { Folder = "WindMedia" }
function MediaManager:GetAsset(url, ext)
    if not url or url == "" then return "" end
    if url:match("^rbxasset") or tonumber(url) then return tonumber(url) and ("rbxassetid://" .. url) or url end
    return url
end
function MediaManager:Image(src) return self:GetAsset(src, "png") end
function MediaManager:Audio(src) return self:GetAsset(src, "mp3") end
function MediaManager:Video(src) return self:GetAsset(src, "webm") end

WindUI.MediaManager = MediaManager

-- Global Exports
if getgenv then
    pcall(function()
        getgenv().WindUI = WindUI
        getgenv().SaveManager = SaveManager
        getgenv().InterfaceManager = InterfaceManager
        getgenv().FloatingButtonManager = FloatingButtonManager
        getgenv().MediaManager = MediaManager
    end)
end

function WindUI:Destroy()
    if self.GUI then pcall(function() self.GUI:Destroy() end) self.GUI = nil end
    if self.ScrollGUI then pcall(function() self.ScrollGUI:Destroy() end) self.ScrollGUI = nil end
    if self.PopupGUI then pcall(function() self.PopupGUI:Destroy() end) self.PopupGUI = nil end
    if self.KeySystemGUI then pcall(function() self.KeySystemGUI:Destroy() end) self.KeySystemGUI = nil end
    self.Unloaded = true
end

return WindUI
""")

output_path = "/home/user/WindUI_Ultimate.lua"
full_code = "\\n".join(code_parts)
with open(output_path, "w", encoding="utf-8") as f:
    f.write(full_code)

line_count = len(full_code.splitlines())
print(f"Successfully generated {output_path} with {line_count} lines of code!")







