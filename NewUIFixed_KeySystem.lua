--[[
    Nexzan Hub UI Library - Edisi Ringkas & Modern (Diperbaiki)
    Dibuat oleh: Nexzan Hub Developer Team
    Deskripsi: Pustaka UI Roblox Premium, Modern, dan Kaya Fitur yang dioptimalkan untuk PC & Mobile.
    Perbaikan: Fitur Seret (Dragging) pada Widget Perkecil kini bekerja 100% lancar di PC & Mobile.
]]

local TweenService = game:GetService("TweenService")
local UserInputService = game:GetService("UserInputService")
local Players = game:GetService("Players")
local MarketPlaceService = game:GetService("MarketplaceService")
local TextService = game:GetService("TextService")
local SoundService = game:GetService("SoundService")

local LocalPlayer = Players.LocalPlayer

-- Konfigurasi Efek Suara
local function playSound(soundId, volume)
    local sound = Instance.new("Sound")
    sound.SoundId = "rbxassetid://" .. tostring(soundId)
    sound.Volume = volume or 0.5
    sound.Parent = SoundService
    sound:Play()
    sound.Ended:Connect(function()
        sound:Destroy()
    end)
end

local Sounds = {
    Click = 6895079853,
    Hover = 6895079632,
    ToggleOn = 8501254395,
    ToggleOff = 8501254199,
    Notification = 9114223297
}

-- Utilitas: Mendapatkan Nama Game Secara Aman
local function getPlaceName()
    local success, info = pcall(function()
        return MarketPlaceService:GetProductInfo(game.PlaceId).Name
    end)
    return success and info or "Game Tidak Dikenal"
end

-- Utilitas: Membuat Gui Dapat Digeser (Drag) Secara Lancar menggunakan Handle Khusus
local function makeDraggable(guiObject, dragHandle)
    dragHandle = dragHandle or guiObject
    local dragging, dragInput, dragStart, startPos

    local function update(input)
        local delta = input.Position - dragStart
        local targetPos = UDim2.new(startPos.X.Scale, startPos.X.Offset + delta.X, startPos.Y.Scale, startPos.Y.Offset + delta.Y)
        TweenService:Create(guiObject, TweenInfo.new(0.15, Enum.EasingStyle.Quad, Enum.EasingDirection.Out), {Position = targetPos}):Play()
    end

    dragHandle.InputBegan:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.MouseButton1 or input.UserInputType == Enum.UserInputType.Touch then
            dragging = true
            dragStart = input.Position
            startPos = guiObject.Position

            input.Changed:Connect(function()
                if input.UserInputState == Enum.UserInputState.End then
                    dragging = false
                end
            end)
        end
    end)

    dragHandle.InputChanged:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.MouseMovement or input.UserInputType == Enum.UserInputType.Touch then
            dragInput = input
        end
    end)

    UserInputService.InputChanged:Connect(function(input)
        if input == dragInput and dragging then
            update(input)
        end
    end)
end

-- Pembuatan Logo "NH" Berdasarkan Gambar (Menggunakan Objek Teks Prosedural)
local function createNHLogo(parent, size, baseTextSize)
    local logoFrame = Instance.new("Frame")
    logoFrame.Name = "NH_Logo"
    logoFrame.Size = size or UDim2.new(0, 42, 0, 42)
    logoFrame.BackgroundTransparency = 1
    logoFrame.Parent = parent

    -- Lingkaran Biru Futuristik
    local ring = Instance.new("Frame")
    ring.Name = "Ring"
    ring.Size = UDim2.new(1, 0, 1, 0)
    ring.BackgroundColor3 = Color3.fromRGB(15, 15, 15)
    ring.BackgroundTransparency = 0.4
    ring.Parent = logoFrame

    local ringCorner = Instance.new("UICorner")
    ringCorner.CornerRadius = UDim.new(1, 0)
    ringCorner.Parent = ring

    local ringStroke = Instance.new("UIStroke")
    ringStroke.Color = Color3.fromRGB(41, 128, 255) -- Biru Terang
    ringStroke.Thickness = 1.6
    ringStroke.Parent = ring

    -- Huruf "N" (Perak / Abu-abu Terang)
    local labelN = Instance.new("TextLabel")
    labelN.Name = "N"
    labelN.Size = UDim2.new(0.6, 0, 0.8, 0)
    labelN.Position = UDim2.new(0.08, 0, 0.08, 0)
    labelN.BackgroundTransparency = 1
    labelN.Font = Enum.Font.GothamBlack
    labelN.Text = "N"
    labelN.TextColor3 = Color3.fromRGB(240, 240, 245)
    labelN.TextSize = baseTextSize or 20
    labelN.TextXAlignment = Enum.TextXAlignment.Center
    labelN.TextYAlignment = Enum.TextYAlignment.Center
    labelN.Parent = logoFrame

    -- Huruf "H" (Biru Elektrik)
    local labelH = Instance.new("TextLabel")
    labelH.Name = "H"
    labelH.Size = UDim2.new(0.6, 0, 0.8, 0)
    labelH.Position = UDim2.new(0.34, 0, 0.14, 0)
    labelH.BackgroundTransparency = 1
    labelH.Font = Enum.Font.GothamBlack
    labelH.Text = "H"
    labelH.TextColor3 = Color3.fromRGB(41, 128, 255)
    labelH.TextSize = baseTextSize or 20
    labelH.TextXAlignment = Enum.TextXAlignment.Center
    labelH.TextYAlignment = Enum.TextYAlignment.Center
    labelH.Parent = logoFrame

    -- Stroke Hitam Tebal untuk memberi Efek Outline/Dimensi (3D Look)
    local strokeN = Instance.new("UIStroke")
    strokeN.Color = Color3.fromRGB(5, 5, 5)
    strokeN.Thickness = 2
    strokeN.Parent = labelN

    local strokeH = Instance.new("UIStroke")
    strokeH.Color = Color3.fromRGB(5, 5, 5)
    strokeH.Thickness = 2
    strokeH.Parent = labelH

    local function adjustTextSize()
        local scaleFactor = logoFrame.AbsoluteSize.Y
        labelN.TextSize = scaleFactor * 0.52
        labelH.TextSize = scaleFactor * 0.52
    end
    logoFrame:GetPropertyChangedSignal("AbsoluteSize"):Connect(adjustTextSize)

    return logoFrame
end

-- Objek Pustaka (Library)
local Library = {}
Library.__index = Library

function Library.new()
    local self = setmetatable({}, Library)
    self.Theme = {
        MainBackground = Color3.fromRGB(15, 15, 15),
        MainBorder = Color3.fromRGB(45, 45, 45),
        LightGrayTrans = Color3.fromRGB(40, 40, 40),
        Accent = Color3.fromRGB(41, 128, 255),
        TextPrimary = Color3.fromRGB(240, 240, 240),
        TextSecondary = Color3.fromRGB(150, 150, 150),
        NotificationColor = Color3.fromRGB(255, 75, 75)
    }
    
    -- Pembuatan Screen GUI Utama
    local screenGui = Instance.new("ScreenGui")
    screenGui.Name = "NexzanHub_ScreenGui"
    screenGui.ResetOnSpawn = false
    screenGui.ZIndexBehavior = Enum.ZIndexBehavior.Sibling
    -- Pastikan halaman System Key selalu berada di atas UI lain.
    screenGui.DisplayOrder = 100
    
    pcall(function()
        screenGui.Parent = game:GetService("CoreGui")
    end)
    if not screenGui.Parent then
        screenGui.Parent = LocalPlayer:WaitForChild("PlayerGui")
    end
    self.ScreenGui = screenGui

    -- Container UI Utama (Lebih Ringkas & Kecil)
    local mainFrame = Instance.new("Frame")
    mainFrame.Name = "MainFrame"
    mainFrame.Size = UDim2.new(0, 480, 0, 310)
    mainFrame.Position = UDim2.new(0.5, -240, 0.5, -155)
    mainFrame.BackgroundColor3 = self.Theme.MainBackground
    mainFrame.BackgroundTransparency = 0.05
    mainFrame.BorderSizePixel = 0
    mainFrame.ClipsDescendants = true
    -- UI utama baru ditampilkan setelah System Key selesai selama 5 detik.
    mainFrame.Visible = false
    mainFrame.Parent = screenGui
    self.MainFrame = mainFrame

    -- Border Bulat & Stroke UI Utama
    local uicorner = Instance.new("UICorner")
    uicorner.CornerRadius = UDim.new(0, 8)
    uicorner.Parent = mainFrame

    local uistroke = Instance.new("UIStroke")
    uistroke.Color = self.Theme.MainBorder
    uistroke.Thickness = 1.2
    uistroke.ApplyStrokeMode = Enum.ApplyStrokeMode.Border
    uistroke.Parent = mainFrame

    makeDraggable(mainFrame)

    -- PANEL KIRI (SIDEBAR KATEGORI)
    local sidebar = Instance.new("Frame")
    sidebar.Name = "Sidebar"
    sidebar.Size = UDim2.new(0, 140, 1, 0)
    sidebar.BackgroundColor3 = self.Theme.LightGrayTrans
    sidebar.BackgroundTransparency = 0.88
    sidebar.BorderSizePixel = 0
    sidebar.Parent = mainFrame

    local sidebarBorder = Instance.new("Frame")
    sidebarBorder.Size = UDim2.new(0, 1, 1, 0)
    sidebarBorder.Position = UDim2.new(1, 0, 0, 0)
    sidebarBorder.BackgroundColor3 = self.Theme.MainBorder
    sidebarBorder.BorderSizePixel = 0
    sidebarBorder.Parent = sidebar

    -- Wadah Logo Prosedural "NH" di Atas Sidebar
    local logoHolder = Instance.new("Frame")
    logoHolder.Name = "LogoHolder"
    logoHolder.Size = UDim2.new(0, 42, 0, 42)
    logoHolder.Position = UDim2.new(0.5, -21, 0, 12)
    logoHolder.BackgroundTransparency = 1
    logoHolder.Parent = sidebar

    createNHLogo(logoHolder, UDim2.new(1, 0, 1, 0), 20)

    -- Bar Pencarian Kategori di Atas Daftar Tab
    local searchContainer = Instance.new("Frame")
    searchContainer.Name = "SearchContainer"
    searchContainer.Size = UDim2.new(0, 120, 0, 24)
    searchContainer.Position = UDim2.new(0.5, -60, 0, 62)
    searchContainer.BackgroundColor3 = self.Theme.MainBackground
    searchContainer.BackgroundTransparency = 0.3
    searchContainer.Parent = sidebar

    local searchCorner = Instance.new("UICorner")
    searchCorner.CornerRadius = UDim.new(0, 5)
    searchCorner.Parent = searchContainer

    local searchStroke = Instance.new("UIStroke")
    searchStroke.Color = self.Theme.MainBorder
    searchStroke.Thickness = 1
    searchStroke.Parent = searchContainer

    local searchBox = Instance.new("TextBox")
    searchBox.Name = "SearchBox"
    searchBox.Size = UDim2.new(1, -10, 1, 0)
    searchBox.Position = UDim2.new(0, 5, 0, 0)
    searchBox.BackgroundTransparency = 1
    searchBox.Font = Enum.Font.SourceSans
    searchBox.TextSize = 12
    searchBox.TextColor3 = self.Theme.TextPrimary
    searchBox.PlaceholderText = "Cari Kategori..."
    searchBox.PlaceholderColor3 = self.Theme.TextSecondary
    searchBox.Text = ""
    searchBox.TextXAlignment = Enum.TextXAlignment.Left
    searchBox.Parent = searchContainer

    -- Area Daftar Tab (Dengan Auto-scroll & Ukuran Proporsional)
    local tabContainer = Instance.new("ScrollingFrame")
    tabContainer.Name = "TabContainer"
    tabContainer.Size = UDim2.new(1, -10, 1, -95)
    tabContainer.Position = UDim2.new(0, 5, 0, 92)
    tabContainer.BackgroundTransparency = 1
    tabContainer.BorderSizePixel = 0
    tabContainer.ScrollBarThickness = 1.5
    tabContainer.ScrollBarImageColor3 = self.Theme.MainBorder
    tabContainer.Parent = sidebar

    local tabLayout = Instance.new("UIListLayout")
    tabLayout.Padding = UDim.new(0, 4)
    tabLayout.HorizontalAlignment = Enum.HorizontalAlignment.Center
    tabLayout.Parent = tabContainer

    tabLayout:GetPropertyChangedSignal("AbsoluteContentSize"):Connect(function()
        tabContainer.CanvasSize = UDim2.new(0, 0, 0, tabLayout.AbsoluteContentSize.Y)
    end)

    -- HEADER ATAS (SISI KANAN)
    local header = Instance.new("Frame")
    header.Name = "Header"
    header.Size = UDim2.new(1, -140, 0, 45)
    header.Position = UDim2.new(0, 140, 0, 0)
    header.BackgroundTransparency = 1
    header.Parent = mainFrame

    local headerBorder = Instance.new("Frame")
    headerBorder.Size = UDim2.new(1, 0, 0, 1)
    headerBorder.Position = UDim2.new(0, 0, 1, 0)
    headerBorder.BackgroundColor3 = self.Theme.MainBorder
    headerBorder.BorderSizePixel = 0
    headerBorder.Parent = header

    -- Teks Deteksi Otomatis Nama Game
    local mapLabel = Instance.new("TextLabel")
    mapLabel.Name = "MapLabel"
    mapLabel.Size = UDim2.new(1, -60, 0, 18)
    mapLabel.Position = UDim2.new(0, 10, 0, 6)
    mapLabel.BackgroundTransparency = 1
    mapLabel.Font = Enum.Font.SourceSansBold
    mapLabel.TextSize = 13
    mapLabel.TextColor3 = self.Theme.TextPrimary
    mapLabel.Text = getPlaceName()
    mapLabel.TextXAlignment = Enum.TextXAlignment.Left
    mapLabel.Parent = header

    -- Teks Pembuat Hub
    local creditLabel = Instance.new("TextLabel")
    creditLabel.Name = "CreditLabel"
    creditLabel.Size = UDim2.new(1, -60, 0, 12)
    creditLabel.Position = UDim2.new(0, 10, 0, 24)
    creditLabel.BackgroundTransparency = 1
    creditLabel.Font = Enum.Font.SourceSansItalic
    creditLabel.TextSize = 10
    creditLabel.TextColor3 = self.Theme.TextSecondary
    creditLabel.Text = "Dibuat oleh Nexzan Hub"
    creditLabel.TextXAlignment = Enum.TextXAlignment.Left
    creditLabel.Parent = header

    -- TOMBOL KONTROL (Perkecil & Tutup)
    local controlFrame = Instance.new("Frame")
    controlFrame.Name = "ControlFrame"
    controlFrame.Size = UDim2.new(0, 50, 0, 25)
    controlFrame.Position = UDim2.new(1, -55, 0, 10)
    controlFrame.BackgroundTransparency = 1
    controlFrame.Parent = header

    local minimizeBtn = Instance.new("TextButton")
    minimizeBtn.Name = "MinimizeBtn"
    minimizeBtn.Size = UDim2.new(0, 20, 0, 20)
    minimizeBtn.Position = UDim2.new(0, 0, 0, 0)
    minimizeBtn.BackgroundColor3 = self.Theme.LightGrayTrans
    minimizeBtn.BackgroundTransparency = 0.5
    minimizeBtn.Font = Enum.Font.SourceSansBold
    minimizeBtn.Text = "-"
    minimizeBtn.TextColor3 = self.Theme.TextPrimary
    minimizeBtn.TextSize = 14
    minimizeBtn.Parent = controlFrame

    local minCorner = Instance.new("UICorner")
    minCorner.CornerRadius = UDim.new(0, 4)
    minCorner.Parent = minimizeBtn

    local minStroke = Instance.new("UIStroke")
    minStroke.Color = self.Theme.MainBorder
    minStroke.Thickness = 1
    minStroke.Parent = minimizeBtn

    local closeBtn = Instance.new("TextButton")
    closeBtn.Name = "CloseBtn"
    closeBtn.Size = UDim2.new(0, 20, 0, 20)
    closeBtn.Position = UDim2.new(0, 24, 0, 0)
    closeBtn.BackgroundColor3 = Color3.fromRGB(200, 50, 50)
    closeBtn.BackgroundTransparency = 0.2
    closeBtn.Font = Enum.Font.SourceSansBold
    closeBtn.Text = "X"
    closeBtn.TextColor3 = Color3.fromRGB(255, 255, 255)
    closeBtn.TextSize = 11
    closeBtn.Parent = controlFrame

    local closeCorner = Instance.new("UICorner")
    closeCorner.CornerRadius = UDim.new(0, 4)
    closeCorner.Parent = closeBtn

    local closeStroke = Instance.new("UIStroke")
    closeStroke.Color = self.Theme.MainBorder
    closeStroke.Thickness = 1
    closeStroke.Parent = closeBtn

    -- AREA KONTEN UTAMA
    local contentArea = Instance.new("Frame")
    contentArea.Name = "ContentArea"
    contentArea.Size = UDim2.new(1, -140, 1, -45)
    contentArea.Position = UDim2.new(0, 140, 0, 45)
    contentArea.BackgroundTransparency = 1
    contentArea.Parent = mainFrame

    -- WIDGET MOBILE MINIMIZE (Sesuai Desain Logo NH Baru)
    local miniWidget = Instance.new("Frame")
    miniWidget.Name = "MiniWidget"
    miniWidget.Size = UDim2.new(0, 45, 0, 45)
    miniWidget.Position = UDim2.new(0, 20, 0.5, -22)
    miniWidget.BackgroundColor3 = self.Theme.MainBackground
    miniWidget.BackgroundTransparency = 0.1
    miniWidget.Active = true -- Diperlukan agar event Input mendeteksi seretan dengan benar
    miniWidget.Visible = false
    miniWidget.Parent = screenGui

    local miniCorner = Instance.new("UICorner")
    miniCorner.CornerRadius = UDim.new(1, 0)
    miniCorner.Parent = miniWidget

    local miniStroke = Instance.new("UIStroke")
    miniStroke.Color = self.Theme.MainBorder
    miniStroke.Thickness = 1.5
    miniStroke.Parent = miniWidget

    -- Logo "NH" Interaktif
    local miniLogoHolder = Instance.new("Frame")
    miniLogoHolder.Name = "MiniLogoHolder"
    miniLogoHolder.Size = UDim2.new(1, 0, 1, 0)
    miniLogoHolder.BackgroundTransparency = 1
    miniLogoHolder.Parent = miniWidget

    createNHLogo(miniLogoHolder, UDim2.new(1, 0, 1, 0), 18)

    -- Tombol klik penuh untuk membuka kembali
    local miniImageBtn = Instance.new("TextButton")
    miniImageBtn.Size = UDim2.new(1, 0, 1, 0)
    miniImageBtn.BackgroundTransparency = 1
    miniImageBtn.Text = ""
    miniImageBtn.Parent = miniWidget

    -- [PERBAIKAN UTAMA]: Menghubungkan fungsi seret ke Tombol Transparan (miniImageBtn)
    -- Ini memungkinkan tombol menelan klik untuk menyeret bingkai induknya (miniWidget).
    makeDraggable(miniWidget, miniImageBtn)

    self.Tabs = {}
    self.ActiveTab = nil

    -- Kontrol Logika Minimalkan / Buka UI
    local isMinimized = false
    local dragThreshold = 5 -- Jarak gerakan minimal sebelum dianggap sebagai seretan (bukan klik biasa)
    local startDragPos

    local function setMinimized(state)
        isMinimized = state
        if isMinimized then
            playSound(Sounds.Click, 0.4)
            mainFrame:TweenSize(UDim2.new(0, 480, 0, 0), "Out", "Quad", 0.3, true, function()
                mainFrame.Visible = false
                miniWidget.Visible = true
            end)
        else
            playSound(Sounds.Click, 0.4)
            mainFrame.Visible = true
            miniWidget.Visible = false
            mainFrame:TweenSize(UDim2.new(0, 480, 0, 310), "Out", "Quad", 0.3, true)
        end
    end

    minimizeBtn.MouseButton1Click:Connect(function()
        setMinimized(true)
    end)

    -- Logika Pencegah Auto-Klik saat widget sedang digeser
    miniImageBtn.InputBegan:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.MouseButton1 or input.UserInputType == Enum.UserInputType.Touch then
            startDragPos = input.Position
        end
    end)

    miniImageBtn.InputEnded:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.MouseButton1 or input.UserInputType == Enum.UserInputType.Touch then
            if startDragPos then
                local dragDistance = (input.Position - startDragPos).Magnitude
                if dragDistance < dragThreshold then
                    -- Hanya buka UI jika widget tidak sedang diseret/digeser
                    setMinimized(false)
                end
            end
        end
    end)

    -- Kontrol Logika Tutup UI Permanen
    closeBtn.MouseButton1Click:Connect(function()
        playSound(Sounds.Click, 0.6)
        screenGui:Destroy()
    end)

    -- Fitur Cari Kategori Secara Real-Time
    searchBox:GetPropertyChangedSignal("Text"):Connect(function()
        local query = string.lower(searchBox.Text)
        for _, tab in ipairs(self.Tabs) do
            if query == "" then
                tab.Button.Visible = true
            else
                if string.find(string.lower(tab.Name), query) then
                    tab.Button.Visible = true
                else
                    tab.Button.Visible = false
                end
            end
        end
    end)

    -- ==================== SYSTEM KEY / LOADING SCREEN ====================
    -- Halaman ini tampil selama 5 detik sebelum UI utama dibuka.
    -- Karena belum ada URL/API validasi key yang diberikan, bagian ini
    -- dibuat sebagai gate/loading screen yang aman dan bisa dikembangkan nanti.
    local keyOverlay = Instance.new("Frame")
    keyOverlay.Name = "KeySystem"
    keyOverlay.Size = UDim2.new(1, 0, 1, 0)
    keyOverlay.Position = UDim2.new(0, 0, 0, 0)
    keyOverlay.BackgroundTransparency = 1
    keyOverlay.BorderSizePixel = 0
    keyOverlay.Active = true
    keyOverlay.ZIndex = 50
    keyOverlay.Parent = screenGui

    local keyPanel = Instance.new("Frame")
    keyPanel.Name = "SourcePanel"
    keyPanel.AnchorPoint = Vector2.new(0.5, 0.5)
    keyPanel.Size = UDim2.new(0, 320, 0, 150)
    keyPanel.Position = UDim2.new(0.5, 0, 0.5, 0)
    keyPanel.BackgroundColor3 = Color3.fromRGB(205, 210, 218)
    keyPanel.BackgroundTransparency = 0.18
    keyPanel.BorderSizePixel = 0
    keyPanel.ZIndex = 51
    keyPanel.Parent = keyOverlay

    local keyPanelCorner = Instance.new("UICorner")
    keyPanelCorner.CornerRadius = UDim.new(0, 10)
    keyPanelCorner.Parent = keyPanel

    local keyPanelStroke = Instance.new("UIStroke")
    keyPanelStroke.Color = self.Theme.Accent
    keyPanelStroke.Thickness = 1.6
    keyPanelStroke.Transparency = 0.22
    keyPanelStroke.ApplyStrokeMode = Enum.ApplyStrokeMode.Border
    keyPanelStroke.Parent = keyPanel

    -- Teks kiri atas
    local hubLabel = Instance.new("TextLabel")
    hubLabel.Name = "HubLabel"
    hubLabel.Size = UDim2.new(0.55, 0, 0, 24)
    hubLabel.Position = UDim2.new(0, 14, 0, 10)
    hubLabel.BackgroundTransparency = 1
    hubLabel.Font = Enum.Font.GothamBold
    hubLabel.Text = "Nexzan Hub"
    hubLabel.TextColor3 = Color3.fromRGB(30, 45, 65)
    hubLabel.TextSize = 14
    hubLabel.TextXAlignment = Enum.TextXAlignment.Left
    hubLabel.ZIndex = 52
    hubLabel.Parent = keyPanel

    -- Teks kanan atas
    local sourceLabel = Instance.new("TextLabel")
    sourceLabel.Name = "SourceLabel"
    sourceLabel.Size = UDim2.new(0.35, 0, 0, 24)
    sourceLabel.Position = UDim2.new(0.65, -14, 0, 10)
    sourceLabel.BackgroundTransparency = 1
    sourceLabel.Font = Enum.Font.GothamSemibold
    sourceLabel.Text = "Source"
    sourceLabel.TextColor3 = self.Theme.Accent
    sourceLabel.TextSize = 13
    sourceLabel.TextXAlignment = Enum.TextXAlignment.Right
    sourceLabel.ZIndex = 52
    sourceLabel.Parent = keyPanel

    local headerLine = Instance.new("Frame")
    headerLine.Name = "HeaderLine"
    headerLine.Size = UDim2.new(1, -28, 0, 1)
    headerLine.Position = UDim2.new(0, 14, 0, 38)
    headerLine.BackgroundColor3 = self.Theme.Accent
    headerLine.BackgroundTransparency = 0.45
    headerLine.BorderSizePixel = 0
    headerLine.ZIndex = 52
    headerLine.Parent = keyPanel

    -- Persentase loading
    local percentLabel = Instance.new("TextLabel")
    percentLabel.Name = "Percent"
    percentLabel.Size = UDim2.new(1, -28, 0, 34)
    percentLabel.Position = UDim2.new(0, 14, 0, 48)
    percentLabel.BackgroundTransparency = 1
    percentLabel.Font = Enum.Font.GothamBold
    percentLabel.Text = "0%"
    percentLabel.TextColor3 = Color3.fromRGB(30, 45, 65)
    percentLabel.TextSize = 24
    percentLabel.TextXAlignment = Enum.TextXAlignment.Center
    percentLabel.TextYAlignment = Enum.TextYAlignment.Center
    percentLabel.ZIndex = 52
    percentLabel.Parent = keyPanel

    -- Bar latar abu-abu terang
    local progressTrack = Instance.new("Frame")
    progressTrack.Name = "ProgressTrack"
    progressTrack.Size = UDim2.new(1, -40, 0, 10)
    progressTrack.Position = UDim2.new(0, 20, 0, 91)
    progressTrack.BackgroundColor3 = Color3.fromRGB(235, 238, 243)
    progressTrack.BackgroundTransparency = 0.22
    progressTrack.BorderSizePixel = 0
    progressTrack.ClipsDescendants = true
    progressTrack.ZIndex = 52
    progressTrack.Parent = keyPanel

    local progressTrackCorner = Instance.new("UICorner")
    progressTrackCorner.CornerRadius = UDim.new(1, 0)
    progressTrackCorner.Parent = progressTrack

    -- Bar biru yang bergerak mengikuti persentase
    local progressFill = Instance.new("Frame")
    progressFill.Name = "ProgressBar"
    progressFill.Size = UDim2.new(0, 0, 1, 0)
    progressFill.BackgroundColor3 = self.Theme.Accent
    progressFill.BackgroundTransparency = 0.04
    progressFill.BorderSizePixel = 0
    progressFill.ZIndex = 53
    progressFill.Parent = progressTrack

    local progressFillCorner = Instance.new("UICorner")
    progressFillCorner.CornerRadius = UDim.new(1, 0)
    progressFillCorner.Parent = progressFill

    local statusLabel = Instance.new("TextLabel")
    statusLabel.Name = "Status"
    statusLabel.Size = UDim2.new(1, -28, 0, 20)
    statusLabel.Position = UDim2.new(0, 14, 0, 111)
    statusLabel.BackgroundTransparency = 1
    statusLabel.Font = Enum.Font.SourceSans
    statusLabel.Text = "Menyiapkan UI..."
    statusLabel.TextColor3 = Color3.fromRGB(65, 75, 90)
    statusLabel.TextSize = 11
    statusLabel.TextXAlignment = Enum.TextXAlignment.Center
    statusLabel.ZIndex = 52
    statusLabel.Parent = keyPanel

    -- API sederhana bila nanti ingin mengakses elemen System Key.
    self.KeySystem = {
        Screen = keyOverlay,
        Panel = keyPanel,
        PercentLabel = percentLabel,
        ProgressBar = progressFill,
        Duration = 5
    }

    -- Satu tween untuk bar dan satu loop ringan untuk memperbarui teks persen.
    TweenService:Create(
        progressFill,
        TweenInfo.new(5, Enum.EasingStyle.Linear, Enum.EasingDirection.Out),
        {Size = UDim2.new(1, 0, 1, 0)}
    ):Play()

    task.spawn(function()
        local startedAt = os.clock()
        local duration = 5

        while screenGui.Parent and keyOverlay.Parent do
            local progress = math.clamp((os.clock() - startedAt) / duration, 0, 1)
            percentLabel.Text = string.format("%d%%", math.floor(progress * 100 + 0.5))

            if progress >= 1 then
                break
            end
            task.wait(0.05)
        end

        -- UI utama baru boleh terbuka setelah 5 detik penuh.
        if screenGui.Parent and keyOverlay.Parent then
            percentLabel.Text = "100%"
            progressFill.Size = UDim2.new(1, 0, 1, 0)
            statusLabel.Text = "Selesai"
            task.wait(0.08)
            keyOverlay:Destroy()
            mainFrame.Visible = true
        end
    end)

    return self
end

-- ==================== FUNGSI BUAT TAB KATEGORI ====================
function Library:CreateTab(tabName, tabIconId)
    local Tab = {
        Name = tabName,
        Elements = {},
        Active = false
    }

    -- Pembuatan Tombol Kategori Tab
    local tabBtn = Instance.new("TextButton")
    tabBtn.Name = tabName .. "_Btn"
    tabBtn.Size = UDim2.new(0, 125, 0, 28)
    tabBtn.BackgroundColor3 = self.Theme.LightGrayTrans
    tabBtn.BackgroundTransparency = 1
    tabBtn.Text = ""
    tabBtn.Parent = self.MainFrame.Sidebar.TabContainer

    local btnCorner = Instance.new("UICorner")
    btnCorner.CornerRadius = UDim.new(0, 6)
    btnCorner.Parent = tabBtn

    local btnStroke = Instance.new("UIStroke")
    btnStroke.Color = self.Theme.MainBorder
    btnStroke.Thickness = 0.8
    btnStroke.Transparency = 1
    btnStroke.Parent = tabBtn

    -- Icon Gambar Tab
    local tabIcon = Instance.new("ImageLabel")
    tabIcon.Name = "Icon"
    tabIcon.Size = UDim2.new(0, 16, 0, 16)
    tabIcon.Position = UDim2.new(0, 8, 0.5, -8)
    tabIcon.BackgroundTransparency = 1
    tabIcon.Image = tabIconId or "rbxassetid://6031075931"
    tabIcon.ImageColor3 = self.Theme.TextSecondary
    tabIcon.Parent = tabBtn

    -- Label Teks Tab
    local tabText = Instance.new("TextLabel")
    tabText.Name = "Label"
    tabText.Size = UDim2.new(1, -40, 1, 0)
    tabText.Position = UDim2.new(0, 30, 0, 0)
    tabText.BackgroundTransparency = 1
    tabText.Font = Enum.Font.SourceSans
    tabText.Text = tabName
    tabText.TextColor3 = self.Theme.TextSecondary
    tabText.TextSize = 12
    tabText.TextXAlignment = Enum.TextXAlignment.Left
    tabText.Parent = tabBtn

    -- Dot Notifikasi Tab
    local notifDot = Instance.new("Frame")
    notifDot.Name = "NotificationDot"
    notifDot.Size = UDim2.new(0, 5, 0, 5)
    notifDot.Position = UDim2.new(1, -12, 0.5, -2.5)
    notifDot.BackgroundColor3 = self.Theme.NotificationColor
    notifDot.BorderSizePixel = 0
    notifDot.Visible = false
    notifDot.Parent = tabBtn

    local dotCorner = Instance.new("UICorner")
    dotCorner.CornerRadius = UDim.new(1, 0)
    dotCorner.Parent = notifDot

    -- Konten Halaman Tab (Daftar Scrolling Frame)
    local page = Instance.new("ScrollingFrame")
    page.Name = tabName .. "_Page"
    page.Size = UDim2.new(1, -16, 1, -16)
    page.Position = UDim2.new(0, 8, 0, 8)
    page.BackgroundTransparency = 1
    page.BorderSizePixel = 0
    page.ScrollBarThickness = 2
    page.ScrollBarImageColor3 = self.Theme.MainBorder
    page.Visible = false
    page.Parent = self.MainFrame.ContentArea

    local pageLayout = Instance.new("UIListLayout")
    pageLayout.Padding = UDim.new(0, 6)
    pageLayout.HorizontalAlignment = Enum.HorizontalAlignment.Center
    pageLayout.Parent = page

    pageLayout:GetPropertyChangedSignal("AbsoluteContentSize"):Connect(function()
        page.CanvasSize = UDim2.new(0, 0, 0, pageLayout.AbsoluteContentSize.Y)
    end)

    Tab.Button = tabBtn
    Tab.Page = page

    -- Logika Navigasi Perpindahan Tab
    local function selectTab()
        playSound(Sounds.Hover, 0.4)
        for _, otherTab in ipairs(self.Tabs) do
            otherTab.Active = false
            otherTab.Page.Visible = false
            TweenService:Create(otherTab.Button, TweenInfo.new(0.2), {BackgroundTransparency = 1}):Play()
            TweenService:Create(otherTab.Button.Label, TweenInfo.new(0.2), {TextColor3 = self.Theme.TextSecondary}):Play()
            TweenService:Create(otherTab.Button.Icon, TweenInfo.new(0.2), {ImageColor3 = self.Theme.TextSecondary}):Play()
            otherTab.Button.UIStroke.Transparency = 1
        end

        Tab.Active = true
        page.Visible = true
        notifDot.Visible = false

        TweenService:Create(tabBtn, TweenInfo.new(0.2), {BackgroundTransparency = 0.85, BackgroundColor3 = self.Theme.LightGrayTrans}):Play()
        TweenService:Create(tabText, TweenInfo.new(0.2), {TextColor3 = self.Theme.TextPrimary}):Play()
        TweenService:Create(tabIcon, TweenInfo.new(0.2), {ImageColor3 = self.Theme.Accent}):Play()
        tabBtn.UIStroke.Transparency = 0.5
    end

    tabBtn.MouseButton1Click:Connect(selectTab)

    table.insert(self.Tabs, Tab)

    if not self.ActiveTab then
        self.ActiveTab = Tab
        selectTab()
    end

    function Tab:ShowNotification()
        notifDot.Visible = true
        playSound(Sounds.Notification, 0.3)
    end

    -- ==================== WIDGET: TOMBOL (BUTTON) ====================
    function Tab:AddButton(title, desc, callback)
        callback = callback or function() end
        
        local buttonFrame = Instance.new("Frame")
        buttonFrame.Name = "Button_" .. title
        buttonFrame.Size = UDim2.new(1, -8, 0, 38)
        buttonFrame.BackgroundColor3 = Color3.fromRGB(20, 20, 20)
        buttonFrame.Parent = page

        local bCorner = Instance.new("UICorner")
        bCorner.CornerRadius = UDim.new(0, 6)
        bCorner.Parent = buttonFrame

        local bStroke = Instance.new("UIStroke")
        bStroke.Color = Color3.fromRGB(45, 45, 45)
        bStroke.Thickness = 1
        bStroke.Parent = buttonFrame

        local titleLabel = Instance.new("TextLabel")
        titleLabel.Size = UDim2.new(0.7, 0, 0, 18)
        titleLabel.Position = UDim2.new(0, 10, 0, 3)
        titleLabel.BackgroundTransparency = 1
        titleLabel.Font = Enum.Font.SourceSansBold
        titleLabel.Text = title
        titleLabel.TextColor3 = Color3.fromRGB(240, 240, 240)
        titleLabel.TextSize = 12
        titleLabel.TextXAlignment = Enum.TextXAlignment.Left
        titleLabel.Parent = buttonFrame

        local descLabel = Instance.new("TextLabel")
        descLabel.Size = UDim2.new(0.7, 0, 0, 14)
        descLabel.Position = UDim2.new(0, 10, 0, 19)
        descLabel.BackgroundTransparency = 1
        descLabel.Font = Enum.Font.SourceSans
        descLabel.Text = desc or "Deskripsi tombol."
        descLabel.TextColor3 = Color3.fromRGB(150, 150, 150)
        descLabel.TextSize = 10
        descLabel.TextXAlignment = Enum.TextXAlignment.Left
        descLabel.Parent = buttonFrame

        local clickBtn = Instance.new("TextButton")
        clickBtn.Size = UDim2.new(0, 65, 0, 22)
        clickBtn.Position = UDim2.new(1, -75, 0.5, -11)
        clickBtn.BackgroundColor3 = Color3.fromRGB(35, 35, 35)
        clickBtn.Text = "Klik"
        clickBtn.TextColor3 = Color3.fromRGB(230, 230, 230)
        clickBtn.Font = Enum.Font.SourceSansBold
        clickBtn.TextSize = 11
        clickBtn.Parent = buttonFrame

        local clickCorner = Instance.new("UICorner")
        clickCorner.CornerRadius = UDim.new(0, 4)
        clickCorner.Parent = clickBtn

        local clickStroke = Instance.new("UIStroke")
        clickStroke.Color = Color3.fromRGB(60, 60, 60)
        clickStroke.Thickness = 1
        clickStroke.Parent = clickBtn

        clickBtn.MouseEnter:Connect(function()
            TweenService:Create(clickBtn, TweenInfo.new(0.2), {BackgroundColor3 = Color3.fromRGB(45, 45, 45)}):Play()
        end)

        clickBtn.MouseLeave:Connect(function()
            TweenService:Create(clickBtn, TweenInfo.new(0.2), {BackgroundColor3 = Color3.fromRGB(35, 35, 35)}):Play()
        end)

        clickBtn.MouseButton1Click:Connect(function()
            playSound(Sounds.Click, 0.5)
            clickBtn.Size = UDim2.new(0, 61, 0, 20)
            clickBtn.Position = UDim2.new(1, -73, 0.5, -10)
            task.wait(0.05)
            clickBtn.Size = UDim2.new(0, 65, 0, 22)
            clickBtn.Position = UDim2.new(1, -75, 0.5, -11)
            pcall(callback)
        end)
    end

    -- ==================== WIDGET: SAKLAR (TOGGLE) ====================
    function Tab:AddToggle(title, desc, default, callback)
        callback = callback or function() end
        local state = default or false

        local toggleFrame = Instance.new("Frame")
        toggleFrame.Name = "Toggle_" .. title
        toggleFrame.Size = UDim2.new(1, -8, 0, 38)
        toggleFrame.BackgroundColor3 = Color3.fromRGB(20, 20, 20)
        toggleFrame.Parent = page

        local tCorner = Instance.new("UICorner")
        tCorner.CornerRadius = UDim.new(0, 6)
        tCorner.Parent = toggleFrame

        local tStroke = Instance.new("UIStroke")
        tStroke.Color = Color3.fromRGB(45, 45, 45)
        tStroke.Thickness = 1
        tStroke.Parent = toggleFrame

        local titleLabel = Instance.new("TextLabel")
        titleLabel.Size = UDim2.new(0.7, 0, 0, 18)
        titleLabel.Position = UDim2.new(0, 10, 0, 3)
        titleLabel.BackgroundTransparency = 1
        titleLabel.Font = Enum.Font.SourceSansBold
        titleLabel.Text = title
        titleLabel.TextColor3 = Color3.fromRGB(240, 240, 240)
        titleLabel.TextSize = 12
        titleLabel.TextXAlignment = Enum.TextXAlignment.Left
        titleLabel.Parent = toggleFrame

        local descLabel = Instance.new("TextLabel")
        descLabel.Size = UDim2.new(0.7, 0, 0, 14)
        descLabel.Position = UDim2.new(0, 10, 0, 19)
        descLabel.BackgroundTransparency = 1
        descLabel.Font = Enum.Font.SourceSans
        descLabel.Text = desc or "Deskripsi saklar."
        descLabel.TextColor3 = Color3.fromRGB(150, 150, 150)
        descLabel.TextSize = 10
        descLabel.TextXAlignment = Enum.TextXAlignment.Left
        descLabel.Parent = toggleFrame

        local toggleSwitch = Instance.new("TextButton")
        toggleSwitch.Size = UDim2.new(0, 34, 0, 18)
        toggleSwitch.Position = UDim2.new(1, -44, 0.5, -9)
        toggleSwitch.BackgroundColor3 = Color3.fromRGB(35, 35, 35)
        toggleSwitch.Text = ""
        toggleSwitch.Parent = toggleFrame

        local tsCorner = Instance.new("UICorner")
        tsCorner.CornerRadius = UDim.new(1, 0)
        tsCorner.Parent = toggleSwitch

        local tsStroke = Instance.new("UIStroke")
        tsStroke.Color = Color3.fromRGB(60, 60, 60)
        tsStroke.Thickness = 1
        tsStroke.Parent = toggleSwitch

        local toggleIndicator = Instance.new("Frame")
        toggleIndicator.Size = UDim2.new(0, 12, 0, 12)
        toggleIndicator.BackgroundColor3 = Color3.fromRGB(200, 200, 200)
        toggleIndicator.Parent = toggleSwitch

        local indCorner = Instance.new("UICorner")
        indCorner.CornerRadius = UDim.new(1, 0)
        indCorner.Parent = toggleIndicator

        local function updateToggle(animate)
            local targetPos = state and UDim2.new(1, -15, 0.5, -6) or UDim2.new(0, 3, 0.5, -6)
            local targetBg = state and Color3.fromRGB(41, 128, 255) or Color3.fromRGB(35, 35, 35)
            
            if animate then
                TweenService:Create(toggleIndicator, TweenInfo.new(0.15, Enum.EasingStyle.Quad), {Position = targetPos}):Play()
                TweenService:Create(toggleSwitch, TweenInfo.new(0.15, Enum.EasingStyle.Quad), {BackgroundColor3 = targetBg}):Play()
                if state then
                    playSound(Sounds.ToggleOn, 0.4)
                else
                    playSound(Sounds.ToggleOff, 0.4)
                end
            else
                toggleIndicator.Position = targetPos
                toggleSwitch.BackgroundColor3 = targetBg
            end
            pcall(callback, state)
        end

        updateToggle(false)

        toggleSwitch.MouseButton1Click:Connect(function()
            state = not state
            updateToggle(true)
        end)
    end

    -- ==================== WIDGET: GESERAN (SLIDER) ====================
    function Tab:AddSlider(title, min, max, default, decimals, callback)
        callback = callback or function() end
        decimals = decimals or 0
        local value = default or min

        local sliderFrame = Instance.new("Frame")
        sliderFrame.Name = "Slider_" .. title
        sliderFrame.Size = UDim2.new(1, -8, 0, 44)
        sliderFrame.BackgroundColor3 = Color3.fromRGB(20, 20, 20)
        sliderFrame.Parent = page

        local sCorner = Instance.new("UICorner")
        sCorner.CornerRadius = UDim.new(0, 6)
        sCorner.Parent = sliderFrame

        local sStroke = Instance.new("UIStroke")
        sStroke.Color = Color3.fromRGB(45, 45, 45)
        sStroke.Thickness = 1
        sStroke.Parent = sliderFrame

        local titleLabel = Instance.new("TextLabel")
        titleLabel.Size = UDim2.new(0.6, 0, 0, 18)
        titleLabel.Position = UDim2.new(0, 10, 0, 3)
        titleLabel.BackgroundTransparency = 1
        titleLabel.Font = Enum.Font.SourceSansBold
        titleLabel.Text = title
        titleLabel.TextColor3 = Color3.fromRGB(240, 240, 240)
        titleLabel.TextSize = 12
        titleLabel.TextXAlignment = Enum.TextXAlignment.Left
        titleLabel.Parent = sliderFrame

        local valBox = Instance.new("TextBox")
        valBox.Size = UDim2.new(0, 40, 0, 16)
        valBox.Position = UDim2.new(1, -50, 0, 4)
        valBox.BackgroundColor3 = Color3.fromRGB(30, 30, 30)
        valBox.Font = Enum.Font.Code
        valBox.TextSize = 10
        valBox.TextColor3 = Color3.fromRGB(240, 240, 240)
        valBox.Text = tostring(value)
        valBox.Parent = sliderFrame

        local boxCorner = Instance.new("UICorner")
        boxCorner.CornerRadius = UDim.new(0, 4)
        boxCorner.Parent = valBox

        local boxStroke = Instance.new("UIStroke")
        boxStroke.Color = Color3.fromRGB(50, 50, 50)
        boxStroke.Parent = valBox

        local track = Instance.new("Frame")
        track.Size = UDim2.new(1, -20, 0, 4)
        track.Position = UDim2.new(0, 10, 0, 28)
        track.BackgroundColor3 = Color3.fromRGB(40, 40, 40)
        track.BorderSizePixel = 0
        track.Parent = sliderFrame

        local trackCorner = Instance.new("UICorner")
        trackCorner.CornerRadius = UDim.new(1, 0)
        trackCorner.Parent = track

        local fill = Instance.new("Frame")
        fill.Size = UDim2.new((value - min)/(max - min), 0, 1, 0)
        fill.BackgroundColor3 = self.Theme.Accent
        fill.BorderSizePixel = 0
        fill.Parent = track

        local fillCorner = Instance.new("UICorner")
        fillCorner.CornerRadius = UDim.new(1, 0)
        fillCorner.Parent = fill

        local knob = Instance.new("Frame")
        knob.Size = UDim2.new(0, 10, 0, 10)
        knob.Position = UDim2.new((value - min)/(max - min), -5, 0.5, -5)
        knob.BackgroundColor3 = Color3.fromRGB(255, 255, 255)
        knob.Parent = track

        local knobCorner = Instance.new("UICorner")
        knobCorner.CornerRadius = UDim.new(1, 0)
        knobCorner.Parent = knob

        local knobStroke = Instance.new("UIStroke")
        knobStroke.Color = Color3.fromRGB(100, 100, 100)
        knobStroke.Thickness = 1
        knobStroke.Parent = knob

        local isSliding = false

        local function updateSlider(inputPos)
            local scale = math.clamp((inputPos - track.AbsolutePosition.X) / track.AbsoluteSize.X, 0, 1)
            local rawVal = min + scale * (max - min)
            local mult = 10^decimals
            value = math.round(rawVal * mult) / mult
            
            fill.Size = UDim2.new(scale, 0, 1, 0)
            knob.Position = UDim2.new(scale, -5, 0.5, -5)
            valBox.Text = tostring(value)
            pcall(callback, value)
        end

        track.InputBegan:Connect(function(input)
            if input.UserInputType == Enum.UserInputType.MouseButton1 or input.UserInputType == Enum.UserInputType.Touch then
                isSliding = true
                updateSlider(input.Position.X)
            end
        end)

        UserInputService.InputChanged:Connect(function(input)
            if isSliding and (input.UserInputType == Enum.UserInputType.MouseMovement or input.UserInputType == Enum.UserInputType.Touch) then
                updateSlider(input.Position.X)
            end
        end)

        UserInputService.InputEnded:Connect(function(input)
            if input.UserInputType == Enum.UserInputType.MouseButton1 or input.UserInputType == Enum.UserInputType.Touch then
                isSliding = false
            end
        end)

        valBox.FocusLost:Connect(function()
            local num = tonumber(valBox.Text)
            if num then
                value = math.clamp(num, min, max)
                local mult = 10^decimals
                value = math.round(value * mult) / mult
                local scale = (value - min) / (max - min)
                TweenService:Create(fill, TweenInfo.new(0.15), {Size = UDim2.new(scale, 0, 1, 0)}):Play()
                TweenService:Create(knob, TweenInfo.new(0.15), {Position = UDim2.new(scale, -5, 0.5, -5)}):Play()
                valBox.Text = tostring(value)
                pcall(callback, value)
            else
                valBox.Text = tostring(value)
            end
        end)
    end

    -- ==================== WIDGET: KOTAK INPUT (TEXTBOX) ====================
    function Tab:AddTextbox(title, placeholder, settings, callback)
        settings = settings or {}
        local numericOnly = settings.NumericOnly or false
        local textOnly = settings.TextOnly or false
        local isPassword = settings.Password or false
        local maxChars = settings.MaxCharacters or 999
        local clearButton = settings.ClearButton or false

        callback = callback or function() end

        local tbFrame = Instance.new("Frame")
        tbFrame.Name = "Textbox_" .. title
        tbFrame.Size = UDim2.new(1, -8, 0, 40)
        tbFrame.BackgroundColor3 = Color3.fromRGB(20, 20, 20)
        tbFrame.Parent = page

        local tbCorner = Instance.new("UICorner")
        tbCorner.CornerRadius = UDim.new(0, 6)
        tbCorner.Parent = tbFrame

        local tbStroke = Instance.new("UIStroke")
        tbStroke.Color = Color3.fromRGB(45, 45, 45)
        tbStroke.Thickness = 1
        tbStroke.Parent = tbFrame

        local titleLabel = Instance.new("TextLabel")
        titleLabel.Size = UDim2.new(0.4, 0, 1, 0)
        titleLabel.Position = UDim2.new(0, 10, 0, 0)
        titleLabel.BackgroundTransparency = 1
        titleLabel.Font = Enum.Font.SourceSansBold
        titleLabel.Text = title
        titleLabel.TextColor3 = Color3.fromRGB(240, 240, 240)
        titleLabel.TextSize = 12
        titleLabel.TextXAlignment = Enum.TextXAlignment.Left
        titleLabel.Parent = tbFrame

        local inputContainer = Instance.new("Frame")
        inputContainer.Size = UDim2.new(0.5, 0, 0, 22)
        inputContainer.Position = UDim2.new(0.5, -5, 0.5, -11)
        inputContainer.BackgroundColor3 = Color3.fromRGB(30, 30, 30)
        inputContainer.Parent = tbFrame

        local icCorner = Instance.new("UICorner")
        icCorner.CornerRadius = UDim.new(0, 4)
        icCorner.Parent = inputContainer

        local icStroke = Instance.new("UIStroke")
        icStroke.Color = Color3.fromRGB(55, 55, 55)
        icStroke.Thickness = 1
        icStroke.Parent = inputContainer

        local tBox = Instance.new("TextBox")
        tBox.Size = UDim2.new(1, -22, 1, 0)
        tBox.Position = UDim2.new(0, 5, 0, 0)
        tBox.BackgroundTransparency = 1
        tBox.Font = Enum.Font.SourceSans
        tBox.PlaceholderText = placeholder or "Ketik di sini..."
        tBox.PlaceholderColor3 = Color3.fromRGB(110, 110, 110)
        tBox.TextColor3 = Color3.fromRGB(240, 240, 240)
        tBox.TextSize = 11
        tBox.Text = ""
        tBox.TextXAlignment = Enum.TextXAlignment.Left
        tBox.Parent = inputContainer

        local clearBtn
        if clearButton then
            clearBtn = Instance.new("TextButton")
            clearBtn.Size = UDim2.new(0, 14, 0, 14)
            clearBtn.Position = UDim2.new(1, -18, 0.5, -7)
            clearBtn.BackgroundTransparency = 1
            clearBtn.Font = Enum.Font.SourceSansBold
            clearBtn.Text = "x"
            clearBtn.TextColor3 = Color3.fromRGB(150, 150, 150)
            clearBtn.TextSize = 11
            clearBtn.Visible = false
            clearBtn.Parent = inputContainer

            clearBtn.MouseButton1Click:Connect(function()
                tBox.Text = ""
                clearBtn.Visible = false
                pcall(callback, "")
            end)
        end

        local shadowText = ""

        tBox:GetPropertyChangedSignal("Text"):Connect(function()
            local text = tBox.Text

            if #text > maxChars then
                text = string.sub(text, 1, maxChars)
                tBox.Text = text
            end

            if numericOnly then
                local filtered = string.gsub(text, "[^%d%.%-]", "")
                if filtered ~= text then
                    text = filtered
                    tBox.Text = text
                end
            elseif textOnly then
                local filtered = string.gsub(text, "[^%a%s]", "")
                if filtered ~= text then
                    text = filtered
                    tBox.Text = text
                end
            end

            if clearBtn then
                clearBtn.Visible = (text ~= "")
            end

            if isPassword then
                shadowText = text
                tBox.Text = string.rep("•", #text)
            else
                shadowText = text
            end
        end)

        tBox.FocusLost:Connect(function()
            pcall(callback, isPassword and shadowText or tBox.Text)
        end)
    end

    -- ==================== WIDGET: PILIHAN (DROPDOWN) ====================
    function Tab:AddDropdown(title, items, isMulti, callback)
        callback = callback or function() end
        local dropdownActive = false
        local selectedItems = {}
        local optionButtons = {}

        local ddFrame = Instance.new("Frame")
        ddFrame.Name = "Dropdown_" .. title
        ddFrame.Size = UDim2.new(1, -8, 0, 38)
        ddFrame.BackgroundColor3 = Color3.fromRGB(20, 20, 20)
        ddFrame.ClipsDescendants = true
        ddFrame.Parent = page

        local ddCorner = Instance.new("UICorner")
        ddCorner.CornerRadius = UDim.new(0, 6)
        ddCorner.Parent = ddFrame

        local ddStroke = Instance.new("UIStroke")
        ddStroke.Color = Color3.fromRGB(45, 45, 45)
        ddStroke.Thickness = 1
        ddStroke.Parent = ddFrame

        local mainButton = Instance.new("TextButton")
        mainButton.Size = UDim2.new(1, 0, 0, 38)
        mainButton.BackgroundTransparency = 1
        mainButton.Text = ""
        mainButton.Parent = ddFrame

        local titleLabel = Instance.new("TextLabel")
        titleLabel.Size = UDim2.new(0.5, 0, 0, 18)
        titleLabel.Position = UDim2.new(0, 10, 0, 3)
        titleLabel.BackgroundTransparency = 1
        titleLabel.Font = Enum.Font.SourceSansBold
        titleLabel.Text = title
        titleLabel.TextColor3 = Color3.fromRGB(240, 240, 240)
        titleLabel.TextSize = 12
        titleLabel.TextXAlignment = Enum.TextXAlignment.Left
        titleLabel.Parent = mainButton

        local selectedLabel = Instance.new("TextLabel")
        selectedLabel.Size = UDim2.new(0.5, 0, 0, 14)
        selectedLabel.Position = UDim2.new(0, 10, 0, 19)
        selectedLabel.BackgroundTransparency = 1
        selectedLabel.Font = Enum.Font.SourceSans
        selectedLabel.Text = "Tidak Ada"
        selectedLabel.TextColor3 = Color3.fromRGB(140, 140, 140)
        selectedLabel.TextSize = 10
        selectedLabel.TextXAlignment = Enum.TextXAlignment.Left
        selectedLabel.Parent = mainButton

        local arrow = Instance.new("ImageLabel")
        arrow.Size = UDim2.new(0, 14, 0, 14)
        arrow.Position = UDim2.new(1, -24, 0.5, -7)
        arrow.BackgroundTransparency = 1
        arrow.Image = "rbxassetid://6031094037"
        arrow.ImageColor3 = Color3.fromRGB(200, 200, 200)
        arrow.Parent = mainButton

        local optionsContainer = Instance.new("ScrollingFrame")
        optionsContainer.Size = UDim2.new(1, -10, 0, 100)
        optionsContainer.Position = UDim2.new(0, 5, 0, 40)
        optionsContainer.BackgroundTransparency = 1
        optionsContainer.BorderSizePixel = 0
        optionsContainer.ScrollBarThickness = 2
        optionsContainer.ScrollBarImageColor3 = Color3.fromRGB(60, 60, 60)
        optionsContainer.Visible = false
        optionsContainer.Parent = ddFrame

        local containerLayout = Instance.new("UIListLayout")
        containerLayout.Padding = UDim.new(0, 3)
        containerLayout.Parent = optionsContainer

        local function updateDropdownLayout()
            optionsContainer.CanvasSize = UDim2.new(0, 0, 0, containerLayout.AbsoluteContentSize.Y)
        end
        containerLayout:GetPropertyChangedSignal("AbsoluteContentSize"):Connect(updateDropdownLayout)

        local function refreshUI()
            if isMulti then
                if #selectedItems == 0 then
                    selectedLabel.Text = "Tidak Ada"
                else
                    selectedLabel.Text = table.concat(selectedItems, ", ")
                end
            else
                selectedLabel.Text = selectedItems[1] or "Tidak Ada"
            end
        end

        local function toggleItem(item)
            if isMulti then
                local idx = table.find(selectedItems, item)
                if idx then
                    table.remove(selectedItems, idx)
                else
                    table.insert(selectedItems, item)
                end
                refreshUI()
                pcall(callback, selectedItems)
            else
                selectedItems = {item}
                refreshUI()
                pcall(callback, item)
                dropdownActive = false
                TweenService:Create(ddFrame, TweenInfo.new(0.2), {Size = UDim2.new(1, -10, 0, 38)}):Play()
                TweenService:Create(arrow, TweenInfo.new(0.2), {Rotation = 0}):Play()
                optionsContainer.Visible = false
            end

            for oName, oBtn in pairs(optionButtons) do
                if table.find(selectedItems, oName) then
                    oBtn.BackgroundColor3 = Color3.fromRGB(60, 60, 60)
                    oBtn.Label.TextColor3 = Color3.fromRGB(255, 255, 255)
                else
                    oBtn.BackgroundColor3 = Color3.fromRGB(25, 25, 25)
                    oBtn.Label.TextColor3 = Color3.fromRGB(180, 180, 180)
                end
            end
        end

        local function renderItems()
            for _, v in pairs(optionsContainer:GetChildren()) do
                if v:IsA("TextButton") then v:Destroy() end
            end
            table.clear(optionButtons)

            for _, item in ipairs(items) do
                local oBtn = Instance.new("TextButton")
                oBtn.Name = item
                oBtn.Size = UDim2.new(1, -5, 0, 22)
                oBtn.BackgroundColor3 = Color3.fromRGB(25, 25, 25)
                oBtn.Text = ""
                oBtn.Parent = optionsContainer

                local oCorner = Instance.new("UICorner")
                oCorner.CornerRadius = UDim.new(0, 4)
                oCorner.Parent = oBtn

                local oLabel = Instance.new("TextLabel")
                oLabel.Name = "Label"
                oLabel.Size = UDim2.new(1, -10, 1, 0)
                oLabel.Position = UDim2.new(0, 8, 0, 0)
                oLabel.BackgroundTransparency = 1
                oLabel.Font = Enum.Font.SourceSans
                oLabel.Text = item
                oLabel.TextColor3 = Color3.fromRGB(180, 180, 180)
                oLabel.TextSize = 11
                oLabel.TextXAlignment = Enum.TextXAlignment.Left
                oLabel.Parent = oBtn

                optionButtons[item] = oBtn

                oBtn.MouseButton1Click:Connect(function()
                    playSound(Sounds.Click, 0.3)
                    toggleItem(item)
                end)
            end
            refreshUI()
        end

        renderItems()

        mainButton.MouseButton1Click:Connect(function()
            playSound(Sounds.Hover, 0.4)
            dropdownActive = not dropdownActive
            if dropdownActive then
                optionsContainer.Visible = true
                TweenService:Create(ddFrame, TweenInfo.new(0.25), {Size = UDim2.new(1, -8, 0, 150)}):Play()
                TweenService:Create(arrow, TweenInfo.new(0.25), {Rotation = 180}):Play()
            else
                TweenService:Create(ddFrame, TweenInfo.new(0.25), {Size = UDim2.new(1, -8, 0, 38)}):Play()
                TweenService:Create(arrow, TweenInfo.new(0.25), {Rotation = 0}):Play()
                task.wait(0.25)
                if not dropdownActive then optionsContainer.Visible = false end
            end
        end)

        local DropdownAPI = {}
        function DropdownAPI:AddItem(item)
            if not table.find(items, item) then
                table.insert(items, item)
                renderItems()
            end
        end

        function DropdownAPI:RemoveItem(item)
            local idx = table.find(items, item)
            if idx then
                table.remove(items, idx)
                local selIdx = table.find(selectedItems, item)
                if selIdx then table.remove(selectedItems, selIdx) end
                renderItems()
            end
        end

        function DropdownAPI:SelectAll()
            if isMulti then
                selectedItems = {unpack(items)}
                renderItems()
                pcall(callback, selectedItems)
            end
        end

        function DropdownAPI:DeselectAll()
            selectedItems = {}
            renderItems()
            pcall(callback, isMulti and {} or "")
        end

        return DropdownAPI
    end

    -- ==================== WIDGET: PILIHAN WARNA ====================
    function Tab:AddColorPicker(title, defaultColor, callback)
        callback = callback or function() end
        local selectedColor = defaultColor or Color3.fromRGB(255, 0, 0)
        local cpActive = false

        local cpFrame = Instance.new("Frame")
        cpFrame.Name = "ColorPicker_" .. title
        cpFrame.Size = UDim2.new(1, -8, 0, 38)
        cpFrame.BackgroundColor3 = Color3.fromRGB(20, 20, 20)
        cpFrame.ClipsDescendants = true
        cpFrame.Parent = page

        local cpCorner = Instance.new("UICorner")
        cpCorner.CornerRadius = UDim.new(0, 6)
        cpCorner.Parent = cpFrame

        local cpStroke = Instance.new("UIStroke")
        cpStroke.Color = Color3.fromRGB(45, 45, 45)
        cpStroke.Thickness = 1
        cpStroke.Parent = cpFrame

        local mainButton = Instance.new("TextButton")
        mainButton.Size = UDim2.new(1, 0, 0, 38)
        mainButton.BackgroundTransparency = 1
        mainButton.Text = ""
        mainButton.Parent = cpFrame

        local titleLabel = Instance.new("TextLabel")
        titleLabel.Size = UDim2.new(0.5, 0, 1, 0)
        titleLabel.Position = UDim2.new(0, 10, 0, 0)
        titleLabel.BackgroundTransparency = 1
        titleLabel.Font = Enum.Font.SourceSansBold
        titleLabel.Text = title
        titleLabel.TextColor3 = Color3.fromRGB(240, 240, 240)
        titleLabel.TextSize = 12
        titleLabel.TextXAlignment = Enum.TextXAlignment.Left
        titleLabel.Parent = mainButton

        local colorPreview = Instance.new("Frame")
        colorPreview.Size = UDim2.new(0, 22, 0, 16)
        colorPreview.Position = UDim2.new(1, -32, 0.5, -8)
        colorPreview.BackgroundColor3 = selectedColor
        colorPreview.Parent = mainButton

        local previewCorner = Instance.new("UICorner")
        previewCorner.CornerRadius = UDim.new(0, 4)
        previewCorner.Parent = colorPreview

        local pickerContainer = Instance.new("Frame")
        pickerContainer.Size = UDim2.new(1, -20, 0, 75)
        pickerContainer.Position = UDim2.new(0, 10, 0, 42)
        pickerContainer.BackgroundTransparency = 1
        pickerContainer.Visible = false
        pickerContainer.Parent = cpFrame

        local function makeRGBSlider(name, colorVal, posIndex)
            local slider = Instance.new("Frame")
            slider.Size = UDim2.new(1, 0, 0, 18)
            slider.Position = UDim2.new(0, 0, 0, (posIndex - 1) * 23)
            slider.BackgroundTransparency = 1
            slider.Parent = pickerContainer

            local label = Instance.new("TextLabel")
            label.Size = UDim2.new(0, 12, 1, 0)
            label.BackgroundTransparency = 1
            label.Font = Enum.Font.Code
            label.Text = name
            label.TextColor3 = Color3.fromRGB(200, 200, 200)
            label.TextSize = 10
            label.Parent = slider

            local track = Instance.new("Frame")
            track.Size = UDim2.new(1, -60, 0, 4)
            track.Position = UDim2.new(0, 18, 0.5, -2)
            track.BackgroundColor3 = Color3.fromRGB(40, 40, 40)
            track.BorderSizePixel = 0
            track.Parent = slider

            local fill = Instance.new("Frame")
            fill.Size = UDim2.new(colorVal, 0, 1, 0)
            fill.BackgroundColor3 = (name == "R" and Color3.fromRGB(220, 50, 50)) or (name == "G" and Color3.fromRGB(50, 220, 50)) or Color3.fromRGB(50, 50, 220)
            fill.Parent = track

            local knob = Instance.new("Frame")
            knob.Size = UDim2.new(0, 8, 0, 8)
            knob.Position = UDim2.new(colorVal, -4, 0.5, -4)
            knob.BackgroundColor3 = Color3.fromRGB(255, 255, 255)
            knob.Parent = track

            local valLabel = Instance.new("TextLabel")
            valLabel.Size = UDim2.new(0, 30, 1, 0)
            valLabel.Position = UDim2.new(1, -35, 0, 0)
            valLabel.BackgroundTransparency = 1
            valLabel.Font = Enum.Font.Code
            valLabel.Text = tostring(math.round(colorVal * 255))
            valLabel.TextColor3 = Color3.fromRGB(200, 200, 200)
            valLabel.TextSize = 10
            valLabel.Parent = slider

            local activeSliding = false
            local function updateRgb(inputPos)
                local scale = math.clamp((inputPos - track.AbsolutePosition.X) / track.AbsoluteSize.X, 0, 1)
                fill.Size = UDim2.new(scale, 0, 1, 0)
                knob.Position = UDim2.new(scale, -4, 0.5, -4)
                valLabel.Text = tostring(math.round(scale * 255))
                
                local r = name == "R" and scale or selectedColor.R
                local g = name == "G" and scale or selectedColor.G
                local b = name == "B" and scale or selectedColor.B
                selectedColor = Color3.new(r, g, b)
                colorPreview.BackgroundColor3 = selectedColor
                pcall(callback, selectedColor)
            end

            track.InputBegan:Connect(function(input)
                if input.UserInputType == Enum.UserInputType.MouseButton1 or input.UserInputType == Enum.UserInputType.Touch then
                    activeSliding = true
                    updateRgb(input.Position.X)
                end
            end)

            UserInputService.InputChanged:Connect(function(input)
                if activeSliding and (input.UserInputType == Enum.UserInputType.MouseMovement or input.UserInputType == Enum.UserInputType.Touch) then
                    updateRgb(input.Position.X)
                end
            end)

            UserInputService.InputEnded:Connect(function(input)
                if input.UserInputType == Enum.UserInputType.MouseButton1 or input.UserInputType == Enum.UserInputType.Touch then
                    activeSliding = false
                end
            end)
        end

        makeRGBSlider("R", selectedColor.R, 1)
        makeRGBSlider("G", selectedColor.G, 2)
        makeRGBSlider("B", selectedColor.B, 3)

        mainButton.MouseButton1Click:Connect(function()
            playSound(Sounds.Hover, 0.3)
            cpActive = not cpActive
            if cpActive then
                pickerContainer.Visible = true
                TweenService:Create(cpFrame, TweenInfo.new(0.2), {Size = UDim2.new(1, -8, 0, 125)}):Play()
            else
                TweenService:Create(cpFrame, TweenInfo.new(0.2), {Size = UDim2.new(1, -8, 0, 38)}):Play()
                task.wait(0.2)
                if not cpActive then pickerContainer.Visible = false end
            end
        end)
    end

    -- ==================== WIDGET: TOMBOL PINTAS (KEYBIND) ====================
    function Tab:AddKeybind(title, defaultKey, callback)
        callback = callback or function() end
        local selectedKey = defaultKey or Enum.KeyCode.E
        local isListening = false

        local kbFrame = Instance.new("Frame")
        kbFrame.Name = "Keybind_" .. title
        kbFrame.Size = UDim2.new(1, -8, 0, 38)
        kbFrame.BackgroundColor3 = Color3.fromRGB(20, 20, 20)
        kbFrame.Parent = page

        local kbCorner = Instance.new("UICorner")
        kbCorner.CornerRadius = UDim.new(0, 6)
        kbCorner.Parent = kbFrame

        local kbStroke = Instance.new("UIStroke")
        kbStroke.Color = Color3.fromRGB(45, 45, 45)
        kbStroke.Thickness = 1
        kbStroke.Parent = kbFrame

        local titleLabel = Instance.new("TextLabel")
        titleLabel.Size = UDim2.new(0.6, 0, 1, 0)
        titleLabel.Position = UDim2.new(0, 10, 0, 0)
        titleLabel.BackgroundTransparency = 1
        titleLabel.Font = Enum.Font.SourceSansBold
        titleLabel.Text = title
        titleLabel.TextColor3 = Color3.fromRGB(240, 240, 240)
        titleLabel.TextSize = 12
        titleLabel.TextXAlignment = Enum.TextXAlignment.Left
        titleLabel.Parent = kbFrame

        local bindBtn = Instance.new("TextButton")
        bindBtn.Size = UDim2.new(0, 65, 0, 22)
        bindBtn.Position = UDim2.new(1, -75, 0.5, -11)
        bindBtn.BackgroundColor3 = Color3.fromRGB(30, 30, 30)
        bindBtn.Font = Enum.Font.Code
        bindBtn.Text = selectedKey.Name
        bindBtn.TextColor3 = Color3.fromRGB(240, 240, 240)
        bindBtn.TextSize = 10
        bindBtn.Parent = kbFrame

        local bindCorner = Instance.new("UICorner")
        bindCorner.CornerRadius = UDim.new(0, 4)
        bindCorner.Parent = bindBtn

        local bindStroke = Instance.new("UIStroke")
        bindStroke.Color = Color3.fromRGB(55, 55, 55)
        bindStroke.Thickness = 1
        bindStroke.Parent = bindBtn

        bindBtn.MouseButton1Click:Connect(function()
            playSound(Sounds.Click, 0.4)
            isListening = true
            bindBtn.Text = "..."
            bindBtn.BackgroundColor3 = Color3.fromRGB(45, 30, 30)
        end)

        UserInputService.InputBegan:Connect(function(input, processed)
            if isListening and not processed then
                if input.UserInputType == Enum.UserInputType.Keyboard then
                    selectedKey = input.KeyCode
                    isListening = false
                    bindBtn.Text = selectedKey.Name
                    bindBtn.BackgroundColor3 = Color3.fromRGB(30, 30, 30)
                end
            elseif not isListening and not processed then
                if input.KeyCode == selectedKey then
                    pcall(callback)
                end
            end
        end)
    end

    -- ==================== WIDGET: LABEL / TEKS ====================
    function Tab:AddLabel(text, richText, animated)
        local labelFrame = Instance.new("Frame")
        labelFrame.Name = "Label_" .. string.sub(text, 1, 8)
        labelFrame.Size = UDim2.new(1, -8, 0, 22)
        labelFrame.BackgroundTransparency = 1
        labelFrame.Parent = page

        local txtLabel = Instance.new("TextLabel")
        txtLabel.Size = UDim2.new(1, -10, 1, 0)
        txtLabel.Position = UDim2.new(0, 5, 0, 0)
        txtLabel.BackgroundTransparency = 1
        txtLabel.Font = Enum.Font.SourceSans
        txtLabel.TextColor3 = Color3.fromRGB(220, 220, 220)
        txtLabel.TextSize = 12
        txtLabel.TextXAlignment = Enum.TextXAlignment.Left
        txtLabel.RichText = richText or false
        txtLabel.Text = text
        txtLabel.Parent = labelFrame

        if animated then
            txtLabel.Text = ""
            task.spawn(function()
                for i = 1, #text do
                    txtLabel.Text = string.sub(text, 1, i)
                    task.wait(0.04)
                end
            end)
        end

        local LabelAPI = {}
        function LabelAPI:SetText(newText)
            txtLabel.Text = newText
        end
        return LabelAPI
    end

    -- ==================== WIDGET: PARAGRAF ====================
    function Tab:AddParagraph(title, description)
        local paraFrame = Instance.new("Frame")
        paraFrame.Name = "Paragraph_" .. title
        paraFrame.Size = UDim2.new(1, -8, 0, 48)
        paraFrame.BackgroundColor3 = Color3.fromRGB(18, 18, 18)
        paraFrame.Parent = page

        local pCorner = Instance.new("UICorner")
        pCorner.CornerRadius = UDim.new(0, 6)
        pCorner.Parent = paraFrame

        local pStroke = Instance.new("UIStroke")
        pStroke.Color = Color3.fromRGB(40, 40, 40)
        pStroke.Thickness = 1
        pStroke.Parent = paraFrame

        local titleLabel = Instance.new("TextLabel")
        titleLabel.Size = UDim2.new(1, -20, 0, 18)
        titleLabel.Position = UDim2.new(0, 10, 0, 4)
        titleLabel.BackgroundTransparency = 1
        titleLabel.Font = Enum.Font.SourceSansBold
        titleLabel.Text = title
        titleLabel.TextColor3 = Color3.fromRGB(240, 240, 240)
        titleLabel.TextSize = 12
        titleLabel.TextXAlignment = Enum.TextXAlignment.Left
        titleLabel.Parent = paraFrame

        local descLabel = Instance.new("TextLabel")
        descLabel.Size = UDim2.new(1, -20, 0, 22)
        descLabel.Position = UDim2.new(0, 10, 0, 20)
        descLabel.BackgroundTransparency = 1
        descLabel.Font = Enum.Font.SourceSans
        descLabel.Text = description
        descLabel.TextColor3 = Color3.fromRGB(160, 160, 160)
        descLabel.TextSize = 10
        descLabel.TextWrapped = true
        descLabel.TextXAlignment = Enum.TextXAlignment.Left
        descLabel.TextYAlignment = Enum.TextYAlignment.Top
        descLabel.Parent = paraFrame
    end

    return Tab
end

return Library
