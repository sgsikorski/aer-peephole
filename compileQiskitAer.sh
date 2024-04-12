cd qiskit-aer

rm -rf _skbuild

# Either option should work to compile the qiskit_aer source code with new additions to the the user's pip env
# Option 1
pip install .

# Option 2
# pip install build
#python -I -m build --wheel

cd ..