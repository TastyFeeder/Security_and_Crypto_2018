#include<Python.h>

int unBitshiftRightXor(int value, int shift);
int unBitshiftLeftXor(int value, int shift, int mask);int r_state(int rand_num);

static PyObject* revers_state(PyObject* self, PyObject * args){
    int input;
    int result;
    PyObject * ret;
    if(!PyArg_ParseTuple(args, "I", &input)){
        return NULL;
    }
    result = r_state(input);
    ret = Py_BuildValue("I",result);
    return ret;
}

static PyObject* next_state(PyObject* self, PyObject * args){
    unsigned long s1;
    unsigned long s2;
    unsigned long result;
    PyObject * ret;
    if(!PyArg_ParseTuple(args, "k|k", &s1,&s2)){
        return NULL;
    }
    result = n_state(s1,s2);
    ret = Py_BuildValue("i",result);
    return ret;
}
static PyMethodDef revers_state_Methods[] = {
    {"revers", revers_state, METH_VARARGS, "revers PRNG state"},
    {"next", next_state, METH_VARARGS, "revers PRNG state"},
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC initrevers_state(void){
    (void) Py_InitModule("revers_state", revers_state_Methods);
}

int n_state(int s1, int s2){
    int y = (s1 & 0x80000000) + (s2 & 0x7fffffff);
    int next = y >> 1;
}

int r_state(int rand_num){
    rand_num = unBitshiftRightXor(rand_num, 18);
    rand_num = unBitshiftLeftXor(rand_num, 15, 0xefc60000);
    rand_num = unBitshiftLeftXor(rand_num, 7, 0x9d2c5680);
    rand_num = unBitshiftRightXor(rand_num, 11); 
    return rand_num;
}

int unBitshiftRightXor(int value, int shift){
    int i = 0 ;
    int result = 0;
    while( i * shift < 32){
        int partMask = (-1 << (32 - shift)) >> (shift * i);
        int part = value & partMask;
        value ^= part >> shift;
        result |= part;
        i++;
    }
    return result;
}


int unBitshiftLeftXor(int value, int shift, int mask) {

    int i = 0 ;
    int result = 0;
    while( i * shift < 32){
        int partMask = (-1 >> (32 - shift)) << (shift * i);
        int part = value & partMask;
        value ^= (part << shift) & mask;
        result |= part;
        i++;
    }
    return result;
}
