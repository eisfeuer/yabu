local Yabu = ug_require "yabu.tl"

function data()
    return {
        bridge = {
            updateFn = function (captureParams, params)
                Yabu.setupModelPartRepository(captureParams.repo)
                local injections = {}

                injections.railing = function (bridge, railingInterval)
                    
                end

                injections.pillar = function (bridge, pillar)
                    
                end

                injections.abutment = function (bridge, abutment)
                    
                end

                local bridge = Yabu.makeBridgeFromParams(params, injections)
                return Yabu.getResultModels(bridge)
            end
        },
    }
end