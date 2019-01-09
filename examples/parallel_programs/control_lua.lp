#script(lua)

function main(prog)
  -- Creo los objetos de control
  local prog1 = clingo.Control({})
  local prog2 = clingo.Control({})

  -- Cargo el primer programa lógico
  prog1:load("example1.lp")
  -- Hago grounding del programa lógico
  prog1:ground({{"base", {}}})
  -- Le digo que al resolver quiero iterar los modelos
  local handle = prog1:solve({yield=true})
  -- Variable en la que guardo los átomos
  local atoms = {}

  -- Itero los modelos
  for m in handle:iter() do
    -- Recorro los átomos del modelo y me quedo solo con los que sean q(N)
    for n in string.gmatch(tostring(m), "q%(%d+%)") do
      table.insert(atoms, n)
    end
  end

  -- Cargo el segundo programa
  prog2:load("example2.lp")
  -- Recorro los atomos obtenidos para guardarlos en un string
  local str = ""
  for k, v in ipairs(atoms) do
    str = str .. v
    if k < # atoms then str = str .. ", "
    else str = str .. "." end
  end
  print(str)
  -- Añado los átomos a la base
  prog2:add("base", {}, str)
  -- Hago el grounding del programa lógico
  prog2:ground({{"base", {}}})
  -- Le digo que al resolver quiero iterar los modelos
  local handle = prog2:solve({yield=true})

  -- Itero los modelos imprimiendo el resultado
  for m in handle:iter() do
    print(m)
    --handle:next()
  end
end

#end.
