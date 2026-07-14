-- Nexzan UI Library
-- Modern Roblox UI Library inspired by WindUI
-- Features: Draggable, Transparent Themes, Many Themes, Scrollable Tabs/Content, Icons by Name, Minimize for Mobile, Tags (changeable), Profile Info, Auto Map Detection, Full Features
-- Logo: NH | Made by Nexzan
-- Version: 1.0

local Library = {}

-- Services
local Players = game:GetService("Players")
local TweenService = game:GetService("TweenService")
local UserInputService = game:GetService("UserInputService")
local RunService = game:GetService("RunService")
local MarketplaceService = game:GetService("MarketplaceService")
local HttpService = game:GetService("HttpService")

local LocalPlayer = Players.LocalPlayer

-- Icon System (Names only, no Asset IDs - using Unicode/Emoji for modern look)
local Icons = {
    -- Common Icons
    home = "🏠",
    settings = "⚙️",
    user = "👤",
    star = "⭐",
    heart = "❤️",
    shield = "🛡️",
    sword = "⚔️",
    target = "🎯",
    eye = "👁️",
    lock = "🔒",
    unlock = "🔓",
    play = "▶️",
    pause = "⏸️",
    stop = "⏹️",
    refresh = "🔄",
    search = "🔍",
    close = "✖️",
    check = "✅",
    warning = "⚠️",
    info = "ℹ️",
    gear = "⚙️",
    menu = "☰",
    arrow_right = "➡️",
    arrow_down = "⬇️",
    plus = "➕",
    minus = "➖",
    trash = "🗑️",
    edit = "✏️",
    save = "💾",
    folder = "📁",
    image = "🖼️",
    music = "🎵",
    video = "📹",
    chat = "💬",
    bell = "🔔",
    flag = "🚩",
    crown = "👑",
    fire = "🔥",
    snow = "❄️",
    sun = "☀️",
    moon = "🌙",
    sparkles = "✨",
    rocket = "🚀",
    map = "🗺️",
    -- Add more as needed
}

-- Theme System - Transparent & Modern
Library.Themes = {
    Dark = {
        Name = "Dark",
        Background = Color3.fromRGB(18, 18, 22),
        Secondary = Color3.fromRGB(28, 28, 34),
        Tertiary = Color3.fromRGB(38, 38, 46),
        Accent = Color3.fromRGB(99, 102, 241), -- Indigo
        AccentDark = Color3.fromRGB(79, 82, 201),
        Text = Color3.fromRGB(240, 240, 245),
        TextDark = Color3.fromRGB(170, 170, 180),
        Border = Color3.fromRGB(55, 55, 65),
        Success = Color3.fromRGB(34, 197, 94),
        Warning = Color3.fromRGB(250, 204, 21),
        Error = Color3.fromRGB(239, 68, 68),
        Transparency = 0.08
    },
    Light = {
        Name = "Light",
        Background = Color3.fromRGB(250, 250, 252),
        Secondary = Color3.fromRGB(240, 240, 245),
        Tertiary = Color3.fromRGB(228, 228, 235),
        Accent = Color3.fromRGB(99, 102, 241),
        AccentDark = Color3.fromRGB(79, 82, 201),
        Text = Color3.fromRGB(30, 30, 35),
        TextDark = Color3.fromRGB(90, 90, 100),
        Border = Color3.fromRGB(200, 200, 210),
        Success = Color3.fromRGB(34, 197, 94),
        Warning = Color3.fromRGB(250, 204, 21),
        Error = Color3.fromRGB(239, 68, 68),
        Transparency = 0.12
    },
    Neon = {
        Name = "Neon",
        Background = Color3.fromRGB(10, 10, 18),
        Secondary = Color3.fromRGB(20, 20, 32),
        Tertiary = Color3.fromRGB(30, 30, 48),
        Accent = Color3.fromRGB(0, 255, 200),
        AccentDark = Color3.fromRGB(0, 200, 160),
        Text = Color3.fromRGB(230, 255, 245),
        TextDark = Color3.fromRGB(160, 190, 180),
        Border = Color3.fromRGB(50, 50, 70),
        Success = Color3.fromRGB(0, 255, 128),
        Warning = Color3.fromRGB(255, 200, 0),
        Error = Color3.fromRGB(255, 80, 80),
        Transparency = 0.06
    },
    Purple = {
        Name = "Purple",
        Background = Color3.fromRGB(22, 18, 32),
        Secondary = Color3.fromRGB(34, 28, 48),
        Tertiary = Color3.fromRGB(46, 38, 62),
        Accent = Color3.fromRGB(167, 139, 250),
        AccentDark = Color3.fromRGB(139, 110, 220),
        Text = Color3.fromRGB(245, 240, 255),
        TextDark = Color3.fromRGB(180, 165, 210),
        Border = Color3.fromRGB(70, 60, 90),
        Success = Color3.fromRGB(52, 211, 153),
        Warning = Color3.fromRGB(251, 191, 36),
        Error = Color3.fromRGB(248, 113, 113),
        Transparency = 0.09
    },
    Ocean = {
        Name = "Ocean",
        Background = Color3.fromRGB(12, 22, 35),
        Secondary = Color3.fromRGB(20, 36, 55),
        Tertiary = Color3.fromRGB(30, 50, 75),
        Accent = Color3.fromRGB(56, 189, 248),
        AccentDark = Color3.fromRGB(14, 165, 233),
        Text = Color3.fromRGB(225, 240, 255),
        TextDark = Color3.fromRGB(160, 185, 210),
        Border = Color3.fromRGB(45, 65, 95),
        Success = Color3.fromRGB(52, 211, 153),
        Warning = Color3.fromRGB(251, 191, 36),
        Error = Color3.fromRGB(248, 113, 113),
        Transparency = 0.07
    },
    Sunset = {
        Name = "Sunset",
        Background = Color3.fromRGB(35, 18, 22),
        Secondary = Color3.fromRGB(50, 26, 32),
        Tertiary = Color3.fromRGB(68, 38, 45),
        Accent = Color3.fromRGB(251, 113, 133),
        AccentDark = Color3.fromRGB(244, 63, 94),
        Text = Color3.fromRGB(255, 235, 235),
        TextDark = Color3.fromRGB(210, 175, 180),
        Border = Color3.fromRGB(90, 55, 60),
        Success = Color3.fromRGB(52, 211, 153),
        Warning = Color3.fromRGB(251, 191, 36),
        Error = Color3.fromRGB(248, 113, 113),
        Transparency = 0.1
    },
    Midnight = {
        Name = "Midnight",
        Background = Color3.fromRGB(8, 10, 20),
        Secondary = Color3.fromRGB(16, 18, 32),
        Tertiary = Color3.fromRGB(26, 28, 46),
        Accent = Color3.fromRGB(129, 140, 248),
        AccentDark = Color3.fromRGB(99, 102, 241),
        Text = Color3.fromRGB(235, 240, 255),
        TextDark = Color3.fromRGB(155, 165, 195),
        Border = Color3.fromRGB(45, 48, 70),
        Success = Color3.fromRGB(34, 197, 94),
        Warning = Color3.fromRGB(250, 204, 21),
        Error = Color3.fromRGB(239, 68, 68),
        Transparency = 0.05
    },
    Emerald = {
        Name = "Emerald",
        Background = Color3.fromRGB(15, 25, 22),
        Secondary = Color3.fromRGB(24, 38, 34),
        Tertiary = Color3.fromRGB(36, 54, 48),
        Accent = Color3.fromRGB(52, 211, 153),
        AccentDark = Color3.fromRGB(16, 185, 129),
        Text = Color3.fromRGB(225, 245, 235),
        TextDark = Color3.fromRGB(155, 190, 175),
        Border = Color3.fromRGB(45, 65, 58),
        Success = Color3.fromRGB(52, 211, 153),
        Warning = Color3.fromRGB(251, 191, 36),
        Error = Color3.fromRGB(248, 113, 113),
        Transparency = 0.08
    }
}

-- Default
Library.CurrentTheme = "Dark"
Library.Transparency = 0.08

-- Utility Functions
local function Create(className, properties)
    local instance = Instance.new(className)
    for prop, value in pairs(properties) do
        if prop ~= "Parent" then
            instance[prop] = value
        end
    end
    if properties.Parent then
        instance.Parent = properties.Parent
    end
    return instance
end

local function Tween(obj, props, duration, style, direction)
    local tween = TweenService:Create(obj, TweenInfo.new(duration or 0.2, style or Enum.EasingStyle.Quint, direction or Enum.EasingDirection.Out), props)
    tween:Play()
    return tween
end

local function ApplyCorner(obj, radius)
    local corner = Create("UICorner", {
        CornerRadius = UDim.new(0, radius or 10),
        Parent = obj
    })
    return corner
end

local function ApplyStroke(obj, thickness, color, transparency)
    local stroke = Create("UIStroke", {
        Thickness = thickness or 1,
        Color = color or Color3.fromRGB(255, 255, 255),
        Transparency = transparency or 0.85,
        Parent = obj
    })
    return stroke
end

local function GetIcon(name)
    if not name then return "●" end
    name = tostring(name):lower()
    return Icons[name] or "●"
end

-- Theme Application
local function ApplyTheme(uiElements, theme)
    if not theme then theme = Library.Themes[Library.CurrentTheme] end
    
    for _, element in pairs(uiElements or {}) do
        if element and element:IsA("GuiObject") then
            pcall(function()
                if element.Name == "MainFrame" or element.Name == "WindowFrame" then
                    element.BackgroundColor3 = theme.Background
                    element.BackgroundTransparency = theme.Transparency
                elseif element.Name:find("Header") or element.Name:find("Sidebar") then
                    element.BackgroundColor3 = theme.Secondary
                    element.BackgroundTransparency = theme.Transparency + 0.05
                elseif element.Name:find("Content") then
                    element.BackgroundColor3 = theme.Tertiary
                    element.BackgroundTransparency = theme.Transparency + 0.1
                elseif element:IsA("TextLabel") or element:IsA("TextButton") or element:IsA("TextBox") then
                    if element.Name:find("Accent") or element.Name == "Logo" then
                        element.TextColor3 = theme.Accent
                    elseif element.Name:find("Title") then
                        element.TextColor3 = theme.Text
                    else
                        element.TextColor3 = theme.TextDark
                    end
                elseif element:IsA("Frame") and element.Name:find("Section") then
                    element.BackgroundColor3 = theme.Tertiary
                    element.BackgroundTransparency = theme.Transparency + 0.15
                end
            end)
        end
    end
end

-- Main Window Creation
function Library:CreateWindow(options)
    options = options or {}
    local Title = options.Title or "Nexzan Hub"
    local Icon = options.Icon or "star"
    local ThemeName = options.Theme or "Dark"
    local Size = options.Size or UDim2.new(0, 620, 0, 420)
    
    if Library.Themes[ThemeName] then
        Library.CurrentTheme = ThemeName
    end
    
    local theme = Library.Themes[Library.CurrentTheme]
    
    -- ScreenGui
    local ScreenGui = Create("ScreenGui", {
        Name = "NexzanUI",
        ResetOnSpawn = false,
        ZIndexBehavior = Enum.ZIndexBehavior.Sibling,
        Parent = game:GetService("CoreGui") -- or LocalPlayer:WaitForChild("PlayerGui")
    })
    
    -- Main Draggable Frame
    local MainFrame = Create("Frame", {
        Name = "MainFrame",
        Size = Size,
        Position = UDim2.new(0.5, -Size.X.Offset/2, 0.5, -Size.Y.Offset/2),
        BackgroundColor3 = theme.Background,
        BackgroundTransparency = theme.Transparency,
        BorderSizePixel = 0,
        Parent = ScreenGui
    })
    ApplyCorner(MainFrame, 16)
    ApplyStroke(MainFrame, 1.5, theme.Border, 0.7)
    
    -- Shadow Effect (using UIStroke for glow-like)
    local Shadow = Create("UIStroke", {
        Thickness = 8,
        Color = Color3.fromRGB(0, 0, 0),
        Transparency = 0.75,
        Parent = MainFrame
    })
    
    -- Header
    local Header = Create("Frame", {
        Name = "Header",
        Size = UDim2.new(1, 0, 0, 54),
        BackgroundColor3 = theme.Secondary,
        BackgroundTransparency = theme.Transparency + 0.05,
        BorderSizePixel = 0,
        Parent = MainFrame
    })
    ApplyCorner(Header, 16)
    
    -- Top bar fix
    local HeaderTop = Create("Frame", {
        Size = UDim2.new(1, 0, 0, 38),
        BackgroundColor3 = theme.Secondary,
        BackgroundTransparency = theme.Transparency + 0.05,
        BorderSizePixel = 0,
        Parent = Header
    })
    
    -- Logo NH
    local LogoFrame = Create("Frame", {
        Name = "LogoFrame",
        Size = UDim2.new(0, 62, 0, 34),
        Position = UDim2.new(0, 12, 0, 8),
        BackgroundColor3 = theme.Accent,
        BackgroundTransparency = 0.1,
        BorderSizePixel = 0,
        Parent = HeaderTop
    })
    ApplyCorner(LogoFrame, 8)
    
    local LogoText = Create("TextLabel", {
        Name = "Logo",
        Size = UDim2.new(1, 0, 1, 0),
        BackgroundTransparency = 1,
        Text = "NH",
        TextColor3 = Color3.fromRGB(255, 255, 255),
        TextSize = 22,
        Font = Enum.Font.GothamBlack,
        TextXAlignment = Enum.TextXAlignment.Center,
        TextYAlignment = Enum.TextYAlignment.Center,
        Parent = LogoFrame
    })
    
    -- Title
    local TitleLabel = Create("TextLabel", {
        Name = "Title",
        Size = UDim2.new(0, 240, 0, 34),
        Position = UDim2.new(0, 82, 0, 8),
        BackgroundTransparency = 1,
        Text = Title,
        TextColor3 = theme.Text,
        TextSize = 18,
        Font = Enum.Font.GothamBold,
        TextXAlignment = Enum.TextXAlignment.Left,
        TextYAlignment = Enum.TextYAlignment.Center,
        Parent = HeaderTop
    })
    
    -- Made by Nexzan
    local MadeBy = Create("TextLabel", {
        Name = "MadeBy",
        Size = UDim2.new(0, 120, 0, 18),
        Position = UDim2.new(0, 82, 0, 32),
        BackgroundTransparency = 1,
        Text = "Made by Nexzan",
        TextColor3 = theme.TextDark,
        TextSize = 11,
        Font = Enum.Font.Gotham,
        TextXAlignment = Enum.TextXAlignment.Left,
        Parent = HeaderTop
    })
    
    -- Profile Info Section (Auto Username, Asli, Foto Profil)
    local ProfileContainer = Create("Frame", {
        Name = "ProfileContainer",
        Size = UDim2.new(0, 145, 0, 34),
        Position = UDim2.new(1, -155, 0, 8),
        BackgroundTransparency = 1,
        Parent = HeaderTop
    })
    
    -- Profile Photo
    local ProfilePhoto = Create("ImageLabel", {
        Name = "ProfilePhoto",
        Size = UDim2.new(0, 28, 0, 28),
        Position = UDim2.new(0, 0, 0, 3),
        BackgroundColor3 = theme.Tertiary,
        BackgroundTransparency = 0.3,
        BorderSizePixel = 0,
        Image = "https://www.roblox.com/headshot-thumbnail/image?userId=" .. LocalPlayer.UserId .. "&width=100&height=100&format=png",
        ScaleType = Enum.ScaleType.Crop,
        Parent = ProfileContainer
    })
    ApplyCorner(ProfilePhoto, 14)
    ApplyStroke(ProfilePhoto, 1, theme.Border, 0.6)
    
    -- Username Info
    local UsernameLabel = Create("TextLabel", {
        Name = "Username",
        Size = UDim2.new(0, 110, 0, 16),
        Position = UDim2.new(0, 34, 0, 1),
        BackgroundTransparency = 1,
        Text = "@" .. LocalPlayer.Name,
        TextColor3 = theme.Text,
        TextSize = 13,
        Font = Enum.Font.GothamBold,
        TextXAlignment = Enum.TextXAlignment.Left,
        TextTruncate = Enum.TextTruncate.AtEnd,
        Parent = ProfileContainer
    })
    
    local DisplayNameLabel = Create("TextLabel", {
        Name = "DisplayName",
        Size = UDim2.new(0, 110, 0, 13),
        Position = UDim2.new(0, 34, 0, 17),
        BackgroundTransparency = 1,
        Text = LocalPlayer.DisplayName .. " • Asli",
        TextColor3 = theme.TextDark,
        TextSize = 10,
        Font = Enum.Font.Gotham,
        TextXAlignment = Enum.TextXAlignment.Left,
        Parent = ProfileContainer
    })
    
    -- Map Name Auto Detect
    local MapLabel = Create("TextLabel", {
        Name = "MapLabel",
        Size = UDim2.new(0, 200, 0, 16),
        Position = UDim2.new(1, -210, 0, 32),
        BackgroundTransparency = 1,
        Text = "🗺️ Loading map...",
        TextColor3 = theme.TextDark,
        TextSize = 10,
        Font = Enum.Font.Gotham,
        TextXAlignment = Enum.TextXAlignment.Right,
        Parent = HeaderTop
    })
    
    -- Auto Detect Map Name
    task.spawn(function()
        local success, info = pcall(function()
            return MarketplaceService:GetProductInfo(game.PlaceId)
        end)
        if success and info then
            MapLabel.Text = "🗺️ " .. (info.Name or game.Name)
        else
            MapLabel.Text = "🗺️ " .. game.Name
        end
    end)
    
    -- Buttons Container
    local HeaderButtons = Create("Frame", {
        Size = UDim2.new(0, 72, 0, 34),
        Position = UDim2.new(1, -78, 0, 8),
        BackgroundTransparency = 1,
        Parent = HeaderTop
    })
    
    -- Minimize Button (For HP/Mobile)
    local MinimizeBtn = Create("TextButton", {
        Name = "MinimizeBtn",
        Size = UDim2.new(0, 28, 0, 28),
        Position = UDim2.new(0, 0, 0, 3),
        BackgroundColor3 = theme.Tertiary,
        BackgroundTransparency = 0.4,
        Text = "–",
        TextColor3 = theme.Text,
        TextSize = 18,
        Font = Enum.Font.GothamBold,
        Parent = HeaderButtons
    })
    ApplyCorner(MinimizeBtn, 6)
    
    -- Close Button
    local CloseBtn = Create("TextButton", {
        Name = "CloseBtn",
        Size = UDim2.new(0, 28, 0, 28),
        Position = UDim2.new(0, 34, 0, 3),
        BackgroundColor3 = theme.Error,
        BackgroundTransparency = 0.2,
        Text = "✕",
        TextColor3 = Color3.fromRGB(255, 255, 255),
        TextSize = 14,
        Font = Enum.Font.GothamBold,
        Parent = HeaderButtons
    })
    ApplyCorner(CloseBtn, 6)
    
    -- Main Content Area
    local ContentArea = Create("Frame", {
        Name = "ContentArea",
        Size = UDim2.new(1, -190, 1, -68),
        Position = UDim2.new(0, 190, 0, 54),
        BackgroundColor3 = theme.Tertiary,
        BackgroundTransparency = theme.Transparency + 0.12,
        BorderSizePixel = 0,
        ClipsDescendants = true,
        Parent = MainFrame
    })
    ApplyCorner(ContentArea, 12)
    
    -- Tabs Sidebar (Scrollable if many tabs)
    local Sidebar = Create("Frame", {
        Name = "Sidebar",
        Size = UDim2.new(0, 180, 1, -68),
        Position = UDim2.new(0, 10, 0, 54),
        BackgroundColor3 = theme.Secondary,
        BackgroundTransparency = theme.Transparency + 0.05,
        BorderSizePixel = 0,
        ClipsDescendants = true,
        Parent = MainFrame
    })
    ApplyCorner(Sidebar, 12)
    
    local TabsContainer = Create("ScrollingFrame", {
        Name = "TabsContainer",
        Size = UDim2.new(1, -10, 1, -10),
        Position = UDim2.new(0, 5, 0, 5),
        BackgroundTransparency = 1,
        BorderSizePixel = 0,
        CanvasSize = UDim2.new(0, 0, 0, 0),
        ScrollBarThickness = 4,
        ScrollBarImageColor3 = theme.Accent,
        Parent = Sidebar
    })
    
    local TabsList = Create("UIListLayout", {
        SortOrder = Enum.SortOrder.LayoutOrder,
        Padding = UDim.new(0, 6),
        Parent = TabsContainer
    })
    
    -- Content Scrolling Frame
    local ContentScroll = Create("ScrollingFrame", {
        Name = "ContentScroll",
        Size = UDim2.new(1, -16, 1, -16),
        Position = UDim2.new(0, 8, 0, 8),
        BackgroundTransparency = 1,
        BorderSizePixel = 0,
        CanvasSize = UDim2.new(0, 0, 0, 0),
        ScrollBarThickness = 5,
        ScrollBarImageColor3 = theme.Accent,
        Parent = ContentArea
    })
    
    local ContentLayout = Create("UIListLayout", {
        SortOrder = Enum.SortOrder.LayoutOrder,
        Padding = UDim.new(0, 10),
        Parent = ContentScroll
    })
    
    -- Auto resize canvas
    ContentLayout:GetPropertyChangedSignal("AbsoluteContentSize"):Connect(function()
        ContentScroll.CanvasSize = UDim2.new(0, 0, 0, ContentLayout.AbsoluteContentSize.Y + 20)
    end)
    
    TabsList:GetPropertyChangedSignal("AbsoluteContentSize"):Connect(function()
        TabsContainer.CanvasSize = UDim2.new(0, 0, 0, TabsList.AbsoluteContentSize.Y + 20)
    end)
    
    -- Tags Container (Horizontal Scroll if many)
    local TagsContainer = Create("Frame", {
        Name = "TagsContainer",
        Size = UDim2.new(1, -20, 0, 28),
        Position = UDim2.new(0, 10, 1, -38),
        BackgroundTransparency = 1,
        ClipsDescendants = true,
        Parent = MainFrame
    })
    
    local TagsScroll = Create("ScrollingFrame", {
        Name = "TagsScroll",
        Size = UDim2.new(1, 0, 1, 0),
        BackgroundTransparency = 1,
        BorderSizePixel = 0,
        CanvasSize = UDim2.new(0, 0, 0, 0),
        ScrollBarThickness = 3,
        ScrollBarImageColor3 = theme.Accent,
        ScrollingDirection = Enum.ScrollingDirection.X,
        Parent = TagsContainer
    })
    
    local TagsLayout = Create("UIListLayout", {
        FillDirection = Enum.FillDirection.Horizontal,
        SortOrder = Enum.SortOrder.LayoutOrder,
        Padding = UDim.new(0, 8),
        Parent = TagsScroll
    })
    
    TagsLayout:GetPropertyChangedSignal("AbsoluteContentSize"):Connect(function()
        TagsScroll.CanvasSize = UDim2.new(0, TagsLayout.AbsoluteContentSize.X + 20, 0, 0)
    end)
    
    -- Internal State
    local Window = {
        ScreenGui = ScreenGui,
        MainFrame = MainFrame,
        Tabs = {},
        CurrentTab = nil,
        Elements = {},
        Tags = {},
        UIElements = {MainFrame, Header, Sidebar, ContentArea, ProfileContainer}
    }
    
    -- Draggable
    local dragging, dragInput, dragStart, startPos
    
    Header.InputBegan:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.MouseButton1 or input.UserInputType == Enum.UserInputType.Touch then
            dragging = true
            dragStart = input.Position
            startPos = MainFrame.Position
        end
    end)
    
    Header.InputChanged:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.MouseMovement or input.UserInputType == Enum.UserInputType.Touch then
            dragInput = input
        end
    end)
    
    UserInputService.InputChanged:Connect(function(input)
        if input == dragInput and dragging then
            local delta = input.Position - dragStart
            MainFrame.Position = UDim2.new(startPos.X.Scale, startPos.X.Offset + delta.X, startPos.Y.Scale, startPos.Y.Offset + delta.Y)
        end
    end)
    
    UserInputService.InputEnded:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.MouseButton1 or input.UserInputType == Enum.UserInputType.Touch then
            dragging = false
        end
    end)
    
    -- Minimize Button Logic (Mobile friendly)
    local minimized = false
    MinimizeBtn.MouseButton1Click:Connect(function()
        minimized = not minimized
        if minimized then
            Tween(MainFrame, {Size = UDim2.new(0, 220, 0, 54)}, 0.25)
            ContentArea.Visible = false
            Sidebar.Visible = false
            TagsContainer.Visible = false
            MinimizeBtn.Text = "+"
        else
            Tween(MainFrame, {Size = Size}, 0.25)
            ContentArea.Visible = true
            Sidebar.Visible = true
            TagsContainer.Visible = true
            MinimizeBtn.Text = "–"
        end
    end)
    
    -- Close Button
    CloseBtn.MouseButton1Click:Connect(function()
        Tween(MainFrame, {Size = UDim2.new(0, 0, 0, 0), Position = UDim2.new(0.5, 0, 0.5, 0)}, 0.2)
        task.wait(0.25)
        ScreenGui:Destroy()
    end)
    
    -- Tab System
    local function CreateTab(tabOptions)
        tabOptions = tabOptions or {}
        local tabTitle = tabOptions.Title or "Tab"
        local tabIcon = GetIcon(tabOptions.Icon or "home")
        
        local TabButton = Create("TextButton", {
            Name = "Tab_" .. tabTitle,
            Size = UDim2.new(1, -8, 0, 38),
            BackgroundColor3 = theme.Tertiary,
            BackgroundTransparency = 0.6,
            Text = "",
            AutoButtonColor = false,
            Parent = TabsContainer
        })
        ApplyCorner(TabButton, 8)
        
        local TabIconLabel = Create("TextLabel", {
            Size = UDim2.new(0, 22, 1, 0),
            Position = UDim2.new(0, 8, 0, 0),
            BackgroundTransparency = 1,
            Text = tabIcon,
            TextColor3 = theme.TextDark,
            TextSize = 18,
            Font = Enum.Font.Gotham,
            TextXAlignment = Enum.TextXAlignment.Center,
            TextYAlignment = Enum.TextYAlignment.Center,
            Parent = TabButton
        })
        
        local TabText = Create("TextLabel", {
            Size = UDim2.new(1, -38, 1, 0),
            Position = UDim2.new(0, 34, 0, 0),
            BackgroundTransparency = 1,
            Text = tabTitle,
            TextColor3 = theme.TextDark,
            TextSize = 13,
            Font = Enum.Font.GothamMedium,
            TextXAlignment = Enum.TextXAlignment.Left,
            TextYAlignment = Enum.TextYAlignment.Center,
            TextTruncate = Enum.TextTruncate.AtEnd,
            Parent = TabButton
        })
        
        -- Tab Content Container
        local TabContent = Create("Frame", {
            Name = "TabContent_" .. tabTitle,
            Size = UDim2.new(1, 0, 1, 0),
            BackgroundTransparency = 1,
            Visible = false,
            Parent = ContentScroll
        })
        
        local TabContentLayout = Create("UIListLayout", {
            SortOrder = Enum.SortOrder.LayoutOrder,
            Padding = UDim.new(0, 8),
            Parent = TabContent
        })
        
        TabContentLayout:GetPropertyChangedSignal("AbsoluteContentSize"):Connect(function()
            -- handled by main scroll
        end)
        
        local tabData = {
            Button = TabButton,
            Content = TabContent,
            Title = tabTitle,
            Icon = tabIcon,
            Sections = {},
            Elements = {}
        }
        
        table.insert(Window.Tabs, tabData)
        
        -- Tab Click
        TabButton.MouseButton1Click:Connect(function()
            for _, t in ipairs(Window.Tabs) do
                t.Button.BackgroundTransparency = 0.6
                t.Button.BackgroundColor3 = theme.Tertiary
                t.Content.Visible = false
            end
            TabButton.BackgroundTransparency = 0.2
            TabButton.BackgroundColor3 = theme.Accent
            TabContent.Visible = true
            Window.CurrentTab = tabData
        end)
        
        -- Hover effects
        TabButton.MouseEnter:Connect(function()
            if Window.CurrentTab ~= tabData then
                Tween(TabButton, {BackgroundTransparency = 0.35}, 0.1)
            end
        end)
        
        TabButton.MouseLeave:Connect(function()
            if Window.CurrentTab ~= tabData then
                Tween(TabButton, {BackgroundTransparency = 0.6}, 0.1)
            end
        end)
        
        -- Select first tab
        if #Window.Tabs == 1 then
            TabButton.BackgroundTransparency = 0.2
            TabButton.BackgroundColor3 = theme.Accent
            TabContent.Visible = true
            Window.CurrentTab = tabData
        end
        
        -- Tab API
        function tabData:CreateSection(sectionTitle)
            local Section = Create("Frame", {
                Name = "Section",
                Size = UDim2.new(1, 0, 0, 36),
                BackgroundColor3 = theme.Tertiary,
                BackgroundTransparency = 0.15,
                BorderSizePixel = 0,
                Parent = self.Content
            })
            ApplyCorner(Section, 10)
            
            local SectionTitle = Create("TextLabel", {
                Name = "SectionTitle",
                Size = UDim2.new(1, -16, 0, 26),
                Position = UDim2.new(0, 12, 0, 6),
                BackgroundTransparency = 1,
                Text = sectionTitle or "Section",
                TextColor3 = theme.Text,
                TextSize = 13,
                Font = Enum.Font.GothamBold,
                TextXAlignment = Enum.TextXAlignment.Left,
                Parent = Section
            })
            
            local SectionContent = Create("Frame", {
                Name = "SectionContent",
                Size = UDim2.new(1, -16, 0, 0),
                Position = UDim2.new(0, 8, 0, 32),
                BackgroundTransparency = 1,
                Parent = Section
            })
            
            local SectionLayout = Create("UIListLayout", {
                SortOrder = Enum.SortOrder.LayoutOrder,
                Padding = UDim.new(0, 6),
                Parent = SectionContent
            })
            
            SectionLayout:GetPropertyChangedSignal("AbsoluteContentSize"):Connect(function()
                Section.Size = UDim2.new(1, 0, 0, SectionLayout.AbsoluteContentSize.Y + 38)
            end)
            
            local sectionData = {
                Frame = Section,
                Content = SectionContent
            }
            
            table.insert(self.Sections, sectionData)
            
            -- Section Element Methods
            function sectionData:AddButton(btnOptions)
                btnOptions = btnOptions or {}
                local btnTitle = btnOptions.Title or "Button"
                local btnCallback = btnOptions.Callback or function() end
                
                local ButtonFrame = Create("Frame", {
                    Size = UDim2.new(1, 0, 0, 36),
                    BackgroundTransparency = 1,
                    Parent = self.Content
                })
                
                local Button = Create("TextButton", {
                    Name = "Button",
                    Size = UDim2.new(1, 0, 1, 0),
                    BackgroundColor3 = theme.Accent,
                    BackgroundTransparency = 0.15,
                    Text = "",
                    AutoButtonColor = false,
                    Parent = ButtonFrame
                })
                ApplyCorner(Button, 8)
                
                local BtnText = Create("TextLabel", {
                    Size = UDim2.new(1, -20, 1, 0),
                    Position = UDim2.new(0, 12, 0, 0),
                    BackgroundTransparency = 1,
                    Text = btnTitle,
                    TextColor3 = Color3.fromRGB(255, 255, 255),
                    TextSize = 13,
                    Font = Enum.Font.GothamMedium,
                    TextXAlignment = Enum.TextXAlignment.Left,
                    Parent = Button
                })
                
                local BtnIcon = Create("TextLabel", {
                    Size = UDim2.new(0, 20, 1, 0),
                    Position = UDim2.new(1, -28, 0, 0),
                    BackgroundTransparency = 1,
                    Text = GetIcon(btnOptions.Icon or "arrow_right"),
                    TextColor3 = Color3.fromRGB(255, 255, 255),
                    TextSize = 15,
                    Font = Enum.Font.Gotham,
                    Parent = Button
                })
                
                Button.MouseButton1Click:Connect(function()
                    Tween(Button, {BackgroundTransparency = 0.4}, 0.08)
                    task.wait(0.1)
                    Tween(Button, {BackgroundTransparency = 0.15}, 0.15)
                    btnCallback()
                end)
                
                return Button
            end
            
            function sectionData:AddToggle(togOptions)
                togOptions = togOptions or {}
                local togTitle = togOptions.Title or "Toggle"
                local togDefault = togOptions.Default or false
                local togCallback = togOptions.Callback or function() end
                
                local ToggleFrame = Create("Frame", {
                    Size = UDim2.new(1, 0, 0, 34),
                    BackgroundTransparency = 1,
                    Parent = self.Content
                })
                
                local ToggleLabel = Create("TextLabel", {
                    Size = UDim2.new(1, -60, 1, 0),
                    Position = UDim2.new(0, 8, 0, 0),
                    BackgroundTransparency = 1,
                    Text = togTitle,
                    TextColor3 = theme.Text,
                    TextSize = 13,
                    Font = Enum.Font.Gotham,
                    TextXAlignment = Enum.TextXAlignment.Left,
                    TextYAlignment = Enum.TextYAlignment.Center,
                    Parent = ToggleFrame
                })
                
                local ToggleSwitch = Create("Frame", {
                    Size = UDim2.new(0, 44, 0, 22),
                    Position = UDim2.new(1, -52, 0.5, -11),
                    BackgroundColor3 = togDefault and theme.Success or theme.Tertiary,
                    BorderSizePixel = 0,
                    Parent = ToggleFrame
                })
                ApplyCorner(ToggleSwitch, 12)
                
                local ToggleKnob = Create("Frame", {
                    Size = UDim2.new(0, 18, 0, 18),
                    Position = togDefault and UDim2.new(1, -20, 0.5, -9) or UDim2.new(0, 2, 0.5, -9),
                    BackgroundColor3 = Color3.fromRGB(255, 255, 255),
                    BorderSizePixel = 0,
                    Parent = ToggleSwitch
                })
                ApplyCorner(ToggleKnob, 9)
                
                local state = togDefault
                
                local function UpdateToggle()
                    Tween(ToggleSwitch, {BackgroundColor3 = state and theme.Success or theme.Tertiary}, 0.15)
                    Tween(ToggleKnob, {Position = state and UDim2.new(1, -20, 0.5, -9) or UDim2.new(0, 2, 0.5, -9)}, 0.15)
                end
                
                ToggleFrame.InputBegan:Connect(function(input)
                    if input.UserInputType == Enum.UserInputType.MouseButton1 or input.UserInputType == Enum.UserInputType.Touch then
                        state = not state
                        UpdateToggle()
                        togCallback(state)
                    end
                end)
                
                return {
                    Set = function(val)
                        state = val
                        UpdateToggle()
                        togCallback(state)
                    end,
                    Get = function() return state end
                }
            end
            
            function sectionData:AddSlider(sliderOptions)
                sliderOptions = sliderOptions or {}
                local sTitle = sliderOptions.Title or "Slider"
                local sMin = sliderOptions.Min or 0
                local sMax = sliderOptions.Max or 100
                local sDefault = sliderOptions.Default or sMin
                local sCallback = sliderOptions.Callback or function() end
                
                local SliderFrame = Create("Frame", {
                    Size = UDim2.new(1, 0, 0, 50),
                    BackgroundTransparency = 1,
                    Parent = self.Content
                })
                
                local SliderLabel = Create("TextLabel", {
                    Size = UDim2.new(1, 0, 0, 18),
                    BackgroundTransparency = 1,
                    Text = sTitle,
                    TextColor3 = theme.Text,
                    TextSize = 12,
                    Font = Enum.Font.Gotham,
                    TextXAlignment = Enum.TextXAlignment.Left,
                    Parent = SliderFrame
                })
                
                local SliderBar = Create("Frame", {
                    Size = UDim2.new(1, -8, 0, 6),
                    Position = UDim2.new(0, 4, 0, 26),
                    BackgroundColor3 = theme.Tertiary,
                    BorderSizePixel = 0,
                    Parent = SliderFrame
                })
                ApplyCorner(SliderBar, 4)
                
                local SliderFill = Create("Frame", {
                    Size = UDim2.new(0, 0, 1, 0),
                    BackgroundColor3 = theme.Accent,
                    BorderSizePixel = 0,
                    Parent = SliderBar
                })
                ApplyCorner(SliderFill, 4)
                
                local SliderValue = Create("TextLabel", {
                    Size = UDim2.new(0, 50, 0, 18),
                    Position = UDim2.new(1, -54, 0, 0),
                    BackgroundTransparency = 1,
                    Text = tostring(sDefault),
                    TextColor3 = theme.TextDark,
                    TextSize = 12,
                    Font = Enum.Font.GothamMedium,
                    TextXAlignment = Enum.TextXAlignment.Right,
                    Parent = SliderFrame
                })
                
                local value = sDefault
                
                local function UpdateSlider(newVal)
                    value = math.clamp(newVal, sMin, sMax)
                    local percent = (value - sMin) / (sMax - sMin)
                    SliderFill.Size = UDim2.new(percent, 0, 1, 0)
                    SliderValue.Text = tostring(math.floor(value))
                    sCallback(value)
                end
                
                UpdateSlider(sDefault)
                
                local draggingSlider = false
                
                SliderBar.InputBegan:Connect(function(input)
                    if input.UserInputType == Enum.UserInputType.MouseButton1 or input.UserInputType == Enum.UserInputType.Touch then
                        draggingSlider = true
                        local percent = math.clamp((input.Position.X - SliderBar.AbsolutePosition.X) / SliderBar.AbsoluteSize.X, 0, 1)
                        UpdateSlider(sMin + (sMax - sMin) * percent)
                    end
                end)
                
                UserInputService.InputChanged:Connect(function(input)
                    if draggingSlider and (input.UserInputType == Enum.UserInputType.MouseMovement or input.UserInputType == Enum.UserInputType.Touch) then
                        local percent = math.clamp((input.Position.X - SliderBar.AbsolutePosition.X) / SliderBar.AbsoluteSize.X, 0, 1)
                        UpdateSlider(sMin + (sMax - sMin) * percent)
                    end
                end)
                
                UserInputService.InputEnded:Connect(function(input)
                    if input.UserInputType == Enum.UserInputType.MouseButton1 or input.UserInputType == Enum.UserInputType.Touch then
                        draggingSlider = false
                    end
                end)
                
                return {
                    Set = UpdateSlider,
                    Get = function() return value end
                }
            end
            
            function sectionData:AddDropdown(ddOptions)
                ddOptions = ddOptions or {}
                local ddTitle = ddOptions.Title or "Dropdown"
                local ddOptionsList = ddOptions.Options or {"Option 1", "Option 2"}
                local ddDefault = ddOptions.Default or ddOptionsList[1]
                local ddCallback = ddOptions.Callback or function() end
                
                local DropdownFrame = Create("Frame", {
                    Size = UDim2.new(1, 0, 0, 34),
                    BackgroundTransparency = 1,
                    Parent = self.Content
                })
                
                local DDLabel = Create("TextLabel", {
                    Size = UDim2.new(1, 0, 0, 18),
                    BackgroundTransparency = 1,
                    Text = ddTitle,
                    TextColor3 = theme.Text,
                    TextSize = 12,
                    Font = Enum.Font.Gotham,
                    TextXAlignment = Enum.TextXAlignment.Left,
                    Parent = DropdownFrame
                })
                
                local DDButton = Create("TextButton", {
                    Size = UDim2.new(1, 0, 0, 28),
                    Position = UDim2.new(0, 0, 0, 18),
                    BackgroundColor3 = theme.Tertiary,
                    Text = ddDefault,
                    TextColor3 = theme.Text,
                    TextSize = 13,
                    Font = Enum.Font.Gotham,
                    TextXAlignment = Enum.TextXAlignment.Left,
                    Parent = DropdownFrame
                })
                ApplyCorner(DDButton, 6)
                
                local DDArrow = Create("TextLabel", {
                    Size = UDim2.new(0, 18, 1, 0),
                    Position = UDim2.new(1, -22, 0, 0),
                    BackgroundTransparency = 1,
                    Text = "▼",
                    TextColor3 = theme.TextDark,
                    TextSize = 11,
                    Parent = DDButton
                })
                
                local DDList = Create("ScrollingFrame", {
                    Size = UDim2.new(1, 0, 0, 0),
                    Position = UDim2.new(0, 0, 1, 4),
                    BackgroundColor3 = theme.Secondary,
                    BorderSizePixel = 0,
                    Visible = false,
                    CanvasSize = UDim2.new(0, 0, 0, 0),
                    ScrollBarThickness = 3,
                    ZIndex = 10,
                    Parent = DropdownFrame
                })
                ApplyCorner(DDList, 6)
                
                local DDListLayout = Create("UIListLayout", {
                    SortOrder = Enum.SortOrder.LayoutOrder,
                    Parent = DDList
                })
                
                local selected = ddDefault
                
                local function ToggleDropdown()
                    DDList.Visible = not DDList.Visible
                    if DDList.Visible then
                        local listHeight = math.min(#ddOptionsList * 26 + 6, 140)
                        DDList.Size = UDim2.new(1, 0, 0, listHeight)
                    end
                end
                
                DDButton.MouseButton1Click:Connect(ToggleDropdown)
                
                for _, opt in ipairs(ddOptionsList) do
                    local OptBtn = Create("TextButton", {
                        Size = UDim2.new(1, 0, 0, 26),
                        BackgroundColor3 = theme.Tertiary,
                        BackgroundTransparency = 0.4,
                        Text = "   " .. opt,
                        TextColor3 = theme.Text,
                        TextSize = 12,
                        Font = Enum.Font.Gotham,
                        TextXAlignment = Enum.TextXAlignment.Left,
                        ZIndex = 10,
                        Parent = DDList
                    })
                    
                    OptBtn.MouseButton1Click:Connect(function()
                        selected = opt
                        DDButton.Text = opt
                        DDList.Visible = false
                        ddCallback(opt)
                    end)
                    
                    OptBtn.MouseEnter:Connect(function()
                        OptBtn.BackgroundTransparency = 0.1
                    end)
                    OptBtn.MouseLeave:Connect(function()
                        OptBtn.BackgroundTransparency = 0.4
                    end)
                end
                
                DDListLayout:GetPropertyChangedSignal("AbsoluteContentSize"):Connect(function()
                    if DDList.Visible then
                        local h = math.min(DDListLayout.AbsoluteContentSize.Y + 6, 140)
                        DDList.Size = UDim2.new(1, 0, 0, h)
                    end
                end)
                
                return {
                    Set = function(val)
                        selected = val
                        DDButton.Text = val
                        ddCallback(val)
                    end
                }
            end
            
            function sectionData:AddTextbox(tbOptions)
                tbOptions = tbOptions or {}
                local tbTitle = tbOptions.Title or "Textbox"
                local tbPlaceholder = tbOptions.Placeholder or "Enter text..."
                local tbDefault = tbOptions.Default or ""
                local tbCallback = tbOptions.Callback or function() end
                
                local TBFrame = Create("Frame", {
                    Size = UDim2.new(1, 0, 0, 52),
                    BackgroundTransparency = 1,
                    Parent = self.Content
                })
                
                local TBLabel = Create("TextLabel", {
                    Size = UDim2.new(1, 0, 0, 18),
                    BackgroundTransparency = 1,
                    Text = tbTitle,
                    TextColor3 = theme.Text,
                    TextSize = 12,
                    Font = Enum.Font.Gotham,
                    TextXAlignment = Enum.TextXAlignment.Left,
                    Parent = TBFrame
                })
                
                local TBInput = Create("TextBox", {
                    Size = UDim2.new(1, 0, 0, 28),
                    Position = UDim2.new(0, 0, 0, 20),
                    BackgroundColor3 = theme.Tertiary,
                    Text = tbDefault,
                    PlaceholderText = tbPlaceholder,
                    TextColor3 = theme.Text,
                    PlaceholderColor3 = theme.TextDark,
                    TextSize = 13,
                    Font = Enum.Font.Gotham,
                    ClearTextOnFocus = false,
                    Parent = TBFrame
                })
                ApplyCorner(TBInput, 6)
                
                TBInput.FocusLost:Connect(function(enter)
                    if enter then
                        tbCallback(TBInput.Text)
                    end
                end)
                
                return TBInput
            end
            
            function sectionData:AddLabel(text)
                local Label = Create("TextLabel", {
                    Size = UDim2.new(1, 0, 0, 22),
                    BackgroundTransparency = 1,
                    Text = text or "Label",
                    TextColor3 = theme.TextDark,
                    TextSize = 12,
                    Font = Enum.Font.Gotham,
                    TextXAlignment = Enum.TextXAlignment.Left,
                    Parent = self.Content
                })
                return Label
            end
            
            function sectionData:AddParagraph(title, content)
                local PFrame = Create("Frame", {
                    Size = UDim2.new(1, 0, 0, 60),
                    BackgroundTransparency = 1,
                    Parent = self.Content
                })
                
                local PTitle = Create("TextLabel", {
                    Size = UDim2.new(1, 0, 0, 18),
                    BackgroundTransparency = 1,
                    Text = title or "Paragraph",
                    TextColor3 = theme.Text,
                    TextSize = 13,
                    Font = Enum.Font.GothamBold,
                    TextXAlignment = Enum.TextXAlignment.Left,
                    Parent = PFrame
                })
                
                local PContent = Create("TextLabel", {
                    Size = UDim2.new(1, 0, 0, 40),
                    Position = UDim2.new(0, 0, 0, 18),
                    BackgroundTransparency = 1,
                    Text = content or "",
                    TextColor3 = theme.TextDark,
                    TextSize = 12,
                    Font = Enum.Font.Gotham,
                    TextXAlignment = Enum.TextXAlignment.Left,
                    TextWrapped = true,
                    Parent = PFrame
                })
                
                return {
                    Update = function(newTitle, newContent)
                        if newTitle then PTitle.Text = newTitle end
                        if newContent then PContent.Text = newContent end
                    end
                }
            end
            
            function sectionData:AddKeybind(kbOptions)
                kbOptions = kbOptions or {}
                local kbTitle = kbOptions.Title or "Keybind"
                local kbDefault = kbOptions.Default or Enum.KeyCode.E
                local kbCallback = kbOptions.Callback or function() end
                
                local KBFrame = Create("Frame", {
                    Size = UDim2.new(1, 0, 0, 36),
                    BackgroundTransparency = 1,
                    Parent = self.Content
                })
                
                local KBLabel = Create("TextLabel", {
                    Size = UDim2.new(1, -70, 1, 0),
                    BackgroundTransparency = 1,
                    Text = kbTitle,
                    TextColor3 = theme.Text,
                    TextSize = 13,
                    Font = Enum.Font.Gotham,
                    TextXAlignment = Enum.TextXAlignment.Left,
                    TextYAlignment = Enum.TextYAlignment.Center,
                    Parent = KBFrame
                })
                
                local KBButton = Create("TextButton", {
                    Size = UDim2.new(0, 62, 0, 24),
                    Position = UDim2.new(1, -68, 0.5, -12),
                    BackgroundColor3 = theme.Tertiary,
                    Text = kbDefault.Name,
                    TextColor3 = theme.Text,
                    TextSize = 11,
                    Font = Enum.Font.GothamMedium,
                    Parent = KBFrame
                })
                ApplyCorner(KBButton, 6)
                
                local listening = false
                local currentKey = kbDefault
                
                KBButton.MouseButton1Click:Connect(function()
                    if listening then return end
                    listening = true
                    KBButton.Text = "..."
                    KBButton.BackgroundColor3 = theme.Accent
                    
                    local conn
                    conn = UserInputService.InputBegan:Connect(function(input)
                        if input.UserInputType == Enum.UserInputType.Keyboard then
                            currentKey = input.KeyCode
                            KBButton.Text = currentKey.Name
                            KBButton.BackgroundColor3 = theme.Tertiary
                            listening = false
                            conn:Disconnect()
                            kbCallback(currentKey)
                        end
                    end)
                end)
                
                return {
                    Set = function(key)
                        currentKey = key
                        KBButton.Text = key.Name
                    end
                }
            end
            
            return sectionData
        end
        
        -- Direct element addition (without section)
        function tabData:AddButton(...) return self:CreateSection():AddButton(...) end
        function tabData:AddToggle(...) return self:CreateSection():AddToggle(...) end
        function tabData:AddSlider(...) return self:CreateSection():AddSlider(...) end
        function tabData:AddDropdown(...) return self:CreateSection():AddDropdown(...) end
        function tabData:AddTextbox(...) return self:CreateSection():AddTextbox(...) end
        function tabData:AddLabel(...) return self:CreateSection():AddLabel(...) end
        function tabData:AddParagraph(...) return self:CreateSection():AddParagraph(...) end
        function tabData:AddKeybind(...) return self:CreateSection():AddKeybind(...) end
        
        return tabData
    end
    
    -- Add Tab function to window
    function Window:Tab(options)
        return CreateTab(options)
    end
    
    -- Tags System (Changeable from outside)
    function Window:AddTag(tagOptions)
        tagOptions = tagOptions or {}
        local tagTitle = tagOptions.Title or "Tag"
        local tagColor = tagOptions.Color or theme.Accent
        
        local Tag = Create("Frame", {
            Size = UDim2.new(0, 0, 0, 22),
            BackgroundColor3 = tagColor,
            BackgroundTransparency = 0.15,
            BorderSizePixel = 0,
            AutomaticSize = Enum.AutomaticSize.X,
            Parent = TagsScroll
        })
        ApplyCorner(Tag, 12)
        
        local TagText = Create("TextLabel", {
            Size = UDim2.new(1, -14, 1, 0),
            Position = UDim2.new(0, 8, 0, 0),
            BackgroundTransparency = 1,
            Text = tagTitle,
            TextColor3 = Color3.fromRGB(255, 255, 255),
            TextSize = 11,
            Font = Enum.Font.GothamMedium,
            TextXAlignment = Enum.TextXAlignment.Center,
            TextYAlignment = Enum.TextYAlignment.Center,
            Parent = Tag
        })
        
        local tagData = {
            Frame = Tag,
            Text = TagText,
            Title = tagTitle,
            Color = tagColor
        }
        
        table.insert(Window.Tags, tagData)
        
        -- API to change
        function tagData:SetTitle(newTitle)
            self.Title = newTitle
            self.Text.Text = newTitle
        end
        
        function tagData:SetColor(newColor)
            self.Color = newColor
            self.Frame.BackgroundColor3 = newColor
        end
        
        return tagData
    end
    
    -- Theme changer
    function Window:SetTheme(themeName)
        if Library.Themes[themeName] then
            Library.CurrentTheme = themeName
            local newTheme = Library.Themes[themeName]
            
            -- Update main colors
            MainFrame.BackgroundColor3 = newTheme.Background
            MainFrame.BackgroundTransparency = newTheme.Transparency
            
            Header.BackgroundColor3 = newTheme.Secondary
            Sidebar.BackgroundColor3 = newTheme.Secondary
            ContentArea.BackgroundColor3 = newTheme.Tertiary
            
            -- Update texts
            TitleLabel.TextColor3 = newTheme.Text
            MadeBy.TextColor3 = newTheme.TextDark
            MapLabel.TextColor3 = newTheme.TextDark
            
            -- Update logo
            LogoFrame.BackgroundColor3 = newTheme.Accent
            
            -- Update all tabs
            for _, tab in ipairs(Window.Tabs) do
                if tab.Button.BackgroundColor3 == theme.Accent then
                    tab.Button.BackgroundColor3 = newTheme.Accent
                end
            end
            
            -- Reapply to profile etc
            ProfilePhoto.BackgroundColor3 = newTheme.Tertiary
        end
    end
    
    -- Get all themes
    function Window:GetThemes()
        local names = {}
        for name, _ in pairs(Library.Themes) do
            table.insert(names, name)
        end
        return names
    end
    
    -- Toggle UI visibility
    function Window:Toggle()
        MainFrame.Visible = not MainFrame.Visible
    end
    
    -- Destroy
    function Window:Destroy()
        ScreenGui:Destroy()
    end
    
    -- Add default profile update if needed
    task.spawn(function()
        task.wait(1)
        -- Refresh profile if needed
        if ProfilePhoto then
            ProfilePhoto.Image = "https://www.roblox.com/headshot-thumbnail/image?userId=" .. LocalPlayer.UserId .. "&width=100&height=100&format=png"
        end
    end)
    
    -- Add some example tags
    Window:AddTag({Title = "VIP", Color = theme.Accent})
    Window:AddTag({Title = "Premium", Color = Color3.fromRGB(251, 191, 36)})
    
    -- Final apply
    table.insert(Window.UIElements, MainFrame)
    
    return Window
end

-- Global helpers
function Library:SetTheme(themeName)
    -- Can be called globally before window creation
    if Library.Themes[themeName] then
        Library.CurrentTheme = themeName
    end
end

function Library:GetThemes()
    local t = {}
    for k, _ in pairs(Library.Themes) do table.insert(t, k) end
    return t
end

-- Notify helper (bonus feature)
function Library:Notify(options)
    options = options or {}
    local notifGui = Instance.new("ScreenGui", game:GetService("CoreGui"))
    local frame = Create("Frame", {
        Size = UDim2.new(0, 280, 0, 60),
        Position = UDim2.new(1, -300, 1, -80),
        BackgroundColor3 = Library.Themes[Library.CurrentTheme].Secondary,
        BackgroundTransparency = 0.1,
        Parent = notifGui
    })
    ApplyCorner(frame, 10)
    
    local title = Create("TextLabel", {
        Size = UDim2.new(1, -20, 0, 22),
        Position = UDim2.new(0, 12, 0, 8),
        BackgroundTransparency = 1,
        Text = options.Title or "Notification",
        TextColor3 = Library.Themes[Library.CurrentTheme].Text,
        TextSize = 13,
        Font = Enum.Font.GothamBold,
        Parent = frame
    })
    
    local desc = Create("TextLabel", {
        Size = UDim2.new(1, -20, 0, 26),
        Position = UDim2.new(0, 12, 0, 28),
        BackgroundTransparency = 1,
        Text = options.Content or "",
        TextColor3 = Library.Themes[Library.CurrentTheme].TextDark,
        TextSize = 11,
        Font = Enum.Font.Gotham,
        Parent = frame
    })
    
    task.delay(options.Duration or 3, function()
        Tween(frame, {Position = UDim2.new(1, 20, 1, -80)}, 0.3)
        task.wait(0.35)
        notifGui:Destroy()
    end)
end

return Library
