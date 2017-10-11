print("NodeMCU running")
wifi.setmode(wifi.STATION)
wifi.sta.config("Hackthon_T4_Station","stevensun")
wifi.sta.connect()

tmr.alarm(1, 1000, 1, function()
     if wifi.sta.getip() == nil then
         print("Connecting...")
     else
         tmr.stop(1)
         print("Connected, IP is "..wifi.sta.getip())
         conn=net.createConnection(net.TCP, false) 
         conn:on("receive", function(conn, pl) print(pl) end)
         conn:connect(4444,"192.168.137.250")
         conn:send("Sensor1 connected")
         dofile("style.lua")
end
end)


