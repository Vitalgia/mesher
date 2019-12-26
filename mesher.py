#!/usr/bin/env python
import argparse
import os
import meshlabxml as mlx

def get_args():
    parser = argparse.ArgumentParser(description='create mesh for a point cloud')
    parser.add_argument('-v', '--meshlab-version', default='2016.2', help='meshlab version')
    parser.add_argument('-p', '--meshlab-path', default='../meshlab/src/distrib/',
                    help='meshlab binaries directory path')

    subparsers = parser.add_subparsers(dest='action')
    bp = subparsers.add_parser('ball-pivoting')
    bp.add_argument('-i', '--input', required=True, help='input file')
    bp.add_argument('-o', '--output', required=True, help='output file')
    bp.add_argument('-r', '--ball-radius', type=float, default=0.127, help="ball radius (algorithm's parameter)")

    poisson = subparsers.add_parser('poisson')
    poisson.add_argument('-i', '--input', required=True, help='input file')
    poisson.add_argument('-o', '--output', required=True, help='output file')
    poisson.add_argument('-d', '--octree-depth', type=int, default=7, help="octtree depth (algorithm's parameter)")
    poisson.add_argument('-s', '--solver-divide', type=int, default=7, help="solver divide (algorithm's parameter)")

    measure = subparsers.add_parser('measure')
    measure.add_argument('-i', '--input', required=True, help='input file')

    return parser.parse_args()


def create_mesh_BALL_PIVOTING(file_in, file_out, ball_radius, ml_version):
    mesher = mlx.FilterScript(file_in=file_in, file_out=file_out, ml_version=ml_version)
    mlx.normals.point_sets(mesher)
    mlx.remesh.ball_pivoting(mesher, ball_radius=ball_radius)
    mesher.run_script()


def create_mesh_POISSON(file_in, file_out, octree_depth, solver_divide, ml_version):
    mesher = mlx.FilterScript(file_in=file_in, file_out=file_out, ml_version=ml_version)
    mlx.normals.point_sets(mesher)
    mlx.remesh.surface_poisson(mesher, octree_depth=octree_depth, solver_divide=solver_divide)
    mesher.run_script()


if __name__ == '__main__':
    args = get_args()
    os.environ['PATH'] = args.meshlab_path + os.pathsep + os.environ['PATH']
    if args.action == 'ball-pivoting':
        create_mesh_BALL_PIVOTING(file_in=args.input, file_out=args.output,
                                  ball_radius=args.ball_radius, ml_version=args.meshlab_version)
    if args.action == 'poisson':
        create_mesh_POISSON(file_in=args.input, file_out=args.output, octree_depth=args.octree_depth,
                            solver_divide=args.solver_divide, ml_version=args.meshlab_version)
    if args.action == 'measure':
        aabb, geometry, topology = mlx.files.measure_all(args.input, ml_version=args.meshlab_version)
        #print(aabb)
        #print(geometry)
        print(topology)





