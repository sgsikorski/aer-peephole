cd qiskit-aer

rm -rf _skbuild

python ./setup.py bdist_wheel -- -DAER_THRUST_BACKEND=CUDA --
pip install -U dist/qiskit_aer*.whl --force-reinstall

cd ..