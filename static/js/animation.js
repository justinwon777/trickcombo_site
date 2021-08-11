import * as THREE from 'https://unpkg.com/three@0.127.0/build/three.module.js';
import { OrbitControls } from 'https://unpkg.com/three@0.127.0/examples/jsm/controls/OrbitControls.js';
import { FBXLoader } from 'https://unpkg.com/three@0.127.0/examples/jsm/loaders/FBXLoader.js';
import { GLTFLoader } from 'https://unpkg.com/three@0.127.0/examples/jsm/loaders/GLTFLoader.js';

let camera, scene, renderer, model;
const clock = new THREE.Clock();
let mixer;

window.createAnimation = function() {
    const body = document.querySelector('#animation-body')
    if (body.hasChildNodes()) {
        body.innerHTML = '';
    }
    init();
//    animate();
}

function init() {

    const container = document.querySelector('#animation-body');
    const width = window.innerWidth - 30;
    const height = window.innerHeight - 170;

    const camera = new THREE.PerspectiveCamera( 50, width / height, 1, 7000);
    camera.position.set(100, 200, 300)

    scene = new THREE.Scene();
    scene.background = new THREE.Color( 0xa0a0a0 );
    scene.fog = new THREE.Fog( 0xa0a0a0, 1, 5000 );

//    const axesHelper = new THREE.AxesHelper( 500 );
//    scene.add( axesHelper );

    const hemiLight = new THREE.HemisphereLight( 0xffffff, 0x444444 );
    hemiLight.position.set( 0, 200, 0 );
    scene.add( hemiLight );

    const dirLight = new THREE.DirectionalLight(0xFFFFFF, 1);
    dirLight.position.set(0, 800, 100);
    dirLight.castShadow = true;
    var d = 1600;
    dirLight.shadow.camera.top = d;
    dirLight.shadow.camera.bottom = -d;
    dirLight.shadow.camera.left = -d;
    dirLight.shadow.camera.right = d;
    dirLight.shadow.camera.near = .01;
    dirLight.shadow.camera.far = 1000;
    scene.add(dirLight);
//    scene.add( new THREE.CameraHelper( dirLight.shadow.camera ) );
//    const dirHelper = new THREE.DirectionalLightHelper(dirLight, 5);
//    scene.add(dirHelper)

    const ground = new THREE.Mesh( new THREE.PlaneGeometry( 10000, 10000 ), new THREE.MeshPhongMaterial({ color: 0xe5e5e5, depthWrite: false }));
    ground.rotation.x = - Math.PI / 2;
    ground.receiveShadow = true;
    scene.add(ground);

    const grid = new THREE.GridHelper( 10000, 50, 0x000000, 0x000000 );
    grid.material.opacity = 0.2;
    grid.material.transparent = true;
    scene.add(grid);

    // model
    const loader = new GLTFLoader();
    loader.load( '../static/mixamo2.gltf', function ( gltf ) {
        model = gltf.scene
        scene.add(model)
        mixer = new THREE.AnimationMixer( model );
        const action1 = mixer.clipAction( gltf.animations[ 3 ] );
        const action2 = mixer.clipAction( gltf.animations[ 2 ] );
        const action3 = mixer.clipAction( gltf.animations[ 5 ] );
//        THREE.AnimationUtils.makeClipAdditive(action2._clip)

        action1
            .setLoop(THREE.LoopOnce)
            .play();
        setTimeout(function() {
            action2
                .crossFadeFrom(action1, 1, true)
                .setLoop(THREE.LoopOnce)
                .play()
        }, action1._clip.duration * 1000 - 500)

//        setTimeout(function() {
//            action3
//                .crossFadeFrom(action2, 1, true)
//                .setLoop(THREE.LoopOnce)
//                .play()
//        }, action1._clip.duration * 1000 - 500 + action2._clip.duration * 1000 - 500)

//        gltf.traverse( function ( child ) {
//            if ( child.isMesh ) {
//                child.castShadow = true;
//                child.receiveShadow = true;
//            }
//        } );
    } );

    renderer = new THREE.WebGLRenderer( { antialias: true } );
    renderer.setPixelRatio( window.devicePixelRatio );
    renderer.setSize( width, height );
    renderer.shadowMap.enabled = true;
    container.appendChild( renderer.domElement );

    const controls = new OrbitControls( camera, renderer.domElement );
    controls.target.set( 0, 100, 0 );
    controls.update();

    function animate() {
        const delta = clock.getDelta();
        if ( mixer ) mixer.update( delta );
        requestAnimationFrame( animate );
        renderer.render( scene, camera );
    }
    requestAnimationFrame( animate );

    window.addEventListener( 'resize', () => {
        const width = window.innerWidth - 30;
        const height = window.innerHeight - 170;

        camera.aspect = width / height;
        camera.updateProjectionMatrix();

        renderer.setSize( width, height );
    });
}
