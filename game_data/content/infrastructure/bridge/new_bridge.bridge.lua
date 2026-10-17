local Yabu = ug_require("yourname_new_bridge::/infrastructure/bridge/yabu.tl")

function data()

local repo = Yabu.initializeModelPartRepository("yourname_new_bridge::/infrastructure/bridge/new_bridge/")

-- Add part models here

return {
	description = {
		name = _("NEW_BRIDGE_NAME"),
		icon = "new_bridge.tga",
	},

	availability = {
		yearFrom = 0,
		yearTo = 0,
	},

	menuCategory = {
		categories = {
			{
                filterCategories = {},
				order = 10000,
			},
		},
	},

	carriers = { "RAIL", "ROAD" },

	speedLimit = 320.0 / 3.6,
	
	pillarLen = 3,
	
	pillarMinDist = 20,
	pillarMaxDist = 160,
	pillarTargetDist = 100,

	cost = 800.0,
	costFactors = { 10.0, 1.76, 4.0 },

	noParallelStripSubdivision = true,
	ignoreWaterCollision = true,

    -- Add a number > 0 to enable abutments
	abutmentLen = 0.0,
	pillarGroundTexture = "::/terrain/materials/dirt/dirt.gtex",
	pillarGroundTextureOffset = 2.0,
	
	materialsToReplace = {	
		streetPaving = {
			name = "::/infrastructure/street/town/mat/town_new_street_paving.mtl",
			size = { 6.0, 6.0 }
		},
		streetLane = {
			name = "::/infrastructure/street/town/mat/town_new_streetlane.mtl",
			size = { 4.0, 5.0 }
		},
		crossingLane = {
			name = "::/infrastructure/street/town/mat/town_new_streetlane.mtl",
		},
		sidewalkPaving = {
			name = "::/infrastructure/street/town/mat/new_medium_sidewalk_paving.mtl",
			size = {32.0,32.0}
		},
		sidewalkBorderInner = {
			name = "::/infrastructure/street/town/mat/new_town_sw_in.mtl",
			size = { 24, 1.5 }
		},
		sidewalkBorderOuter = {
			name = "::/infrastructure/street/town/mat/new_town_sw_in.mtl",
			size = { 24, 1.5 },
			reversed = true,
		},
		sidewalkCurb = {
			name = "::/infrastructure/street/town/mat/new_town_sw_curb.mtl",
			size = { 24, .35 }
		},
		sidewalkWall  = {
			name = "",
			size = {24,0.35}
		},
	},

	assetsToReplace = {
        -- Uncomment if bridge should not have street lights
		--["street_light"] = {}
	},
	
	updateScript = {
		fileName = "new_bridge.script@bridge.updateFn",
		params = {
			repo = repo
		}
	},
}

end
