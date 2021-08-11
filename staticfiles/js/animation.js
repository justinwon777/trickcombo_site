import * as THREE from 'https://unpkg.com/three/build/three.module.js';
import { OrbitControls } from 'https://unpkg.com/three/examples/jsm/controls/OrbitControls.js';
import { FBXLoader } from 'https://unpkg.com/three/examples/jsm/loaders/FBXLoader.js';

let camera, scene, renderer;
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
    const loader = new FBXLoader();
    loader.load( '../static/Backflip.fbx', function ( object ) {
        mixer = new THREE.AnimationMixer( object );
        const action = mixer.clipAction( object.animations[ 0 ] );
        action.play();
//        object.traverse( function ( child ) {
//            if ( child.isMesh ) {
//                child.castShadow = true;
//                child.receiveShadow = true;
//            }
//        } );
        scene.add( object );
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
        requestAnimationFrame( animate );
        const delta = clock.getDelta();
        if ( mixer ) mixer.update( delta );
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
