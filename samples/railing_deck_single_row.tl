-- Deck assembly pattern:
-- One row spans the full railing interval. The left and right side parts are
-- placed at the outer width positions and scaled along X to the interval
-- length. Repeated center parts fill the space between them and are scaled
-- along X and Y to fit the interval length and width. Curvature is ignored.

local transf: Mat4Serialized = ug_require("::/scripts/mat4.tl")

local Yabu = ug_require("eisfeuer_bietigheimer::/infrastructure/bridge/yabu.tl")

-- creates transformation matrix for part models
-- @param scaleX part model x scale
-- @param scaleY part model y scale
-- @param xPos part model x position
-- @param yPos part model y position
-- @return calculated transformation matrix
local function makeTransform(scaleX: number, scaleY: number, xPos: number, yPos: number): Mat4
    return transf.scaleXYZRotZTransl(
        { x = scaleX, y = scaleY, z = 1},
        0,
        { x = xPos, y = yPos, z = 0}
    )
end

-- railing section params
local record Params is Yabu.RailingParamsInterface
    repo: Yabu.PartModelRepository -- given part model repository
    bridge: Yabu.BridgeParams -- original bridge params
    interval: Yabu.RailingInterval -- railing interval param from the injection function
end

-- deck section
local record Deck is Yabu.RailingSectionInterface
    buildAndGetRailingSectionModel: function(Params): Yabu.RailingSectionModel
end

-- builds a railing section and returns the model list
-- @param input (see RailingParamsInterface above)
-- @return A list of all part models for the railing section
function Deck.buildAndGetRailingSectionModel(p: Params): Yabu.RailingSectionModel
    local rowModel: Yabu.RailingRowModel = {}
    local interval = p.interval

    if interval.length <= 0 or interval.width <= 0 then
        return { rowModel }
    end

    -- get necessary part models
    local sideL: Yabu.PartModel = p.repo.railingDeckSideL
    local sideR: Yabu.PartModel = p.repo.railingDeckSideR
    local rep: Yabu.PartModel = p.repo.railingDeckRep

    -- get lane offset
    local avgLaneOffset = p.interval.yabu.avgLaneOffset

    -- calculate optimal amount of rows, row scales, and row sizes
    local rowData: Yabu.RailingRowData = {
        x = Yabu.calculateOptimalRowSize(p.interval.length,  rep.bb.size.x, { fixedAmountOfRows = 1 }),
        y = Yabu.calculateOptimalRowSize(p.interval.width, rep.bb.size.y)
    }

    -- add left part model to row
    table.insert(rowModel, {
        id = sideL.id,
        transf = makeTransform(rowData.x.rowScale, 1, 0, -p.interval.width * 0.5 + avgLaneOffset),
    })

    -- add repeating part models to row
    for iY = 0, rowData.y.amountOfRows - 1 do
        local yPos = -interval.width * 0.5 + iY * rowData.y.rowLength
        table.insert(rowModel, {
            id = rep.id,
            transf = makeTransform(rowData.x.rowScale, rowData.y.rowScale, 0, yPos + avgLaneOffset),
        })
    end

    -- add right part model to row
    table.insert(rowModel, {
        id = sideR.id,
        transf = makeTransform(rowData.x.rowScale, 1, 0, interval.width * 0.5 + avgLaneOffset),
    })

    return { rowModel }
end

return Deck