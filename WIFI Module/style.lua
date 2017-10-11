uart.setup(0, 9600, 8, 0, 1, 1)
uart.on("data", 0,
  function(data)
    --print("receive from uart:", data)
    conn:send(data)
    if data=="$quit" then
      uart.on("data") -- unregister callback function
    end
end, 0)