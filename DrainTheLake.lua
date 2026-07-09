local WindUI = loadstring(game:HttpGet("https://github.com/Footagesus/WindUI/releases/latest/download/main.lua"))()

local Version = "2.0.0.1"
local WindUI = loadstring(game:HttpGet("https://github.com/Footagesus/WindUI/releases/download/" .. Version .. "/main.lua"))()

WindUI:AddTheme({
    Name = "My Theme", -- theme name
    
    
    -- More Soon!
    
    Accent = Color3.fromHex("#18181b"),
    Background = Color3.fromHex("#101010"), -- Accent
    BackgroundTransparency = 0,
    Outline = Color3.fromHex("#FFFFFF"),
    Text = Color3.fromHex("#FFFFFF"),
    Placeholder = Color3.fromHex("#7a7a7a"),
    Button = Color3.fromHex("#52525b"),
    Icon = Color3.fromHex("#a1a1aa"),
    
    Hover = Color3.fromHex("#FFFFFF"), -- Text
    BackgroundTransparency = 0,
    
    WindowBackground = Color3.fromHex("101010"), -- Background
    WindowShadow = Color3.fromHex("000000"),
    
    DialogBackground = Color3.fromHex("#101010"), -- Background
    DialogBackgroundTransparency = 0, -- BackgroundTransparency
    DialogTitle = Color3.fromHex("#FFFFFF"), -- Text
    DialogContent = Color3.fromHex("#FFFFFF"), -- Text
    DialogIcon = Color3.fromHex("#a1a1aa"), -- Icon
    
    WindowTopbarButtonIcon = Color3.fromHex("a1a1aa"), -- Icon
    WindowTopbarTitle = Color3.fromHex("FFFFFF"), -- Text
    WindowTopbarAuthor = Color3.fromHex("FFFFFF"), -- Text
    WindowTopbarIcon = Color3.fromHex("FFFFFF"), -- Text
    
    TabBackground = Color3.fromHex("#FFFFFF"), -- Text
    TabTitle = Color3.fromHex("#FFFFFF"), -- Text
    TabIcon = Color3.fromHex("a1a1aa"), -- Icon
    
    ElementBackground = Color3.fromHex("#FFFFFF"), -- Text
    ElementTitle = Color3.fromHex("#FFFFFF"), -- Text
    ElementDesc = Color3.fromHex("#FFFFFF"), -- Text
    ElementIcon = Color3.fromHex("#a1a1aa"), -- Icon
    
    PopupBackground = Color3.fromHex("#101010"), -- Background
    PopupBackgroundTransparency = 0, -- BackgroundTransparency
    PopupTitle = Color3.fromHex("#FFFFFF"), -- Text
    PopupContent = Color3.fromHex("#FFFFFF"), -- Text
    PopupIcon = Color3.fromHex("#a1a1aa"), -- Icon
    
    DialogBackground = Color3.fromHex("#101010"), -- Background
    DialogBackgroundTransparency = 0, -- Transparency
    DialogTitle = Color3.fromHex("#FFFFFF"), -- Text
    DialogContent = Color3.fromHex("#FFFFFF"), -- Text
    DialogIcon = Color3.fromHex("#a1a1aa"), -- Icon
    
    Toggle = Color3.fromHex("#52525b"), -- Button
    ToggleBar = Color3.fromHex("#FFFFFF"), -- White
    
    Checkbox = Color3.fromHex("#52525b"), -- Button
    CheckboxIcon = Color3.fromHex("#FFFFFF"), -- White
    
    Slider = Color3.fromHex("#52525b"), -- Button
    SliderThumb = Color3.fromHex("#FFFFFF"), -- White
    
})

local Window = WindUI:CreateWindow({
    Title = "Drain The Lake",
    Icon = "door-open", -- lucide icon. optional
    Author = "Made Nexzan Hub", -- optional
})

Window:EditOpenButton({
    Title = "Open UI",
    Icon = "monitor",
    CornerRadius = UDim.new(0,16),
    StrokeThickness = 2,
    Color = ColorSequence.new( -- gradient
        Color3.fromHex("FF0F7B"), 
        Color3.fromHex("F89B29")
    ),
    OnlyMobile = false,
    Enabled = true,
    Draggable = true,
})

local Tab = Window:Tab({
    Title = "Fram",
    Icon = "bird", -- optional
    Locked = false,
})

Window:Tag({
    Title = "v1.6.6",
    Icon = "github",
    Color = Color3.fromHex("#30ff6a"),
    Radius = 0, -- from 0 to 13
})

-- 1. Fitur Auto Fill Water
Tab:Toggle({
    Title = "Auto Fill Water",
    Desc = "Otomatis mengisi ember air",
    Icon = "droplet",
    Value = false,
    Callback = function(state)
        _G.AutoFill = state
        task.spawn(function()
            while _G.AutoFill do
                pcall(function() 
                    game:GetService("ReplicatedStorage").VerdantRemotes["VDT_Bucket.Used"]:FireServer() 
                end)
                task.wait(0.1)
            end
        end)
    end
})

-- 2. Fitur Auto Pour Bucket
Tab:Toggle({
    Title = "Auto Pour Bucket",
    Desc = "Otomatis menuang air ke checkpoint",
    Icon = "cup-water",
    Value = false,
    Callback = function(state)
        _G.AutoPour = state
        task.spawn(function()
            while _G.AutoPour do
                if Player.Character and Player.Character:FindFirstChild("HumanoidRootPart") then 
                    Player.Character.HumanoidRootPart.CFrame = TargetPos 
                end
                pcall(function() 
                    local prompt = workspace.Scripted.CheckpointParts["1"]:GetChildren()[3].Scripted.ProximityPosition.ProximityPrompt
                    prompt:InputHoldBegin()
                    prompt:InputHoldEnd()
                end)
                task.wait(0.3)
            end
        end)
    end
})

-- 3. Fitur Auto Take Tokens
Tab:Toggle({
    Title = "Auto Take Tokens",
    Desc = "Otomatis mengambil token",
    Icon = "coins",
    Value = false,
    Callback = function(state)
        _G.AutoToken = state
        task.spawn(function()
            while _G.AutoToken do
                if Player.Character and Player.Character:FindFirstChild("HumanoidRootPart") then 
                    Player.Character.HumanoidRootPart.CFrame = TargetPos 
                end
                pcall(function() 
                    local prompt = workspace.Scripted.CheckpointParts["1"]:GetChildren()[3].Scripted.TakeTokens.ProximityPrompt
                    prompt:InputHoldBegin()
                    prompt:InputHoldEnd()
                end)
                task.wait(0.3)
            end
        end)
    end
})
