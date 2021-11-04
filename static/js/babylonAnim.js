window.addEventListener("DOMContentLoaded", function() {
    var canvas = document.getElementById("renderCanvas");

    var engine = new BABYLON.Engine(canvas, true);
    
    const createScene =  () => {
        const scene = new BABYLON.Scene(engine);

        const camera = new BABYLON.ArcRotateCamera("camera", -Math.PI / 2, Math.PI / 2.5, 15, new BABYLON.Vector3(0, 0, 0));
        camera.attachControl(canvas, true);
        const light = new BABYLON.HemisphericLight("light", new BABYLON.Vector3(1, 1, 0));

        BABYLON.SceneLoader.LoadAssetContainer("../static/", "mixamo3.gltf", scene, function (container) {
            var character = container.meshes[0]
            var animations = container.animationGroups
            animations[0].stop()
            animations[1].start(false)
            animations[0].start(true)
            container.addAllToScene()
        })

        return scene;
    }

    const scene = createScene()

    engine.runRenderLoop(() => {
        scene.render()
    })

    window.addEventListener("resize", function() {
        engine.resize()
    })
})