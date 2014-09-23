
import ResultObjs, os

def margeParamTex(rootname, params=None, limit=1, paramNameFile=None):
    """ Get tex snipped for constraint on parameters in params """
    if not '.margestats' in rootname: rootname += '.margestats'
    marge = ResultObjs.margeStats(rootname , paramNameFile)
    if not params: params = marge.list()

    formatter = ResultObjs.noLineTableFormatter()
    texs = []
    labels = []
    for par in params:
        tex = marge.texValues(formatter, par, limit=limit)
        if tex is not None:
            texs.append(tex[0])
            labels.append(marge.parWithName(par).label)
        else:
            texs.append(None)
            labels.append(None)

    return params, labels, texs

def makeSnippetFiles(outdir, rootname, params, texs, tag=None):
    """ make separate tex file for each parameter, e.g. for inclusion in paper """
    base = os.path.splitext(os.path.basename(rootname))[0]
    for param, tex in zip(params, texs):
        fname = base + '-' + param
        if tag is not None: fname += '_' + tag
        with open(os.path.join(outdir, fname + '.tex'), 'w') as f:
            f.write(tex)


if __name__ == "__main__":
    import argparse
#    import batchJobArgs

    parser = argparse.ArgumentParser(description='make latex constraints for specific .margestats file')
    parser.add_argument('rootname', help='rootname.margestats should be the file you want to convert')
    parser.add_argument('--params', nargs='*', help='list of parameter name tags; if not supplied, output all parameters')
    parser.add_argument('--limit', type=int, default=1, help='which limit to output, usually 1: 1 sigma or 2: 2 sigma')
    parser.add_argument('--tex_snippet_dir', help='output a .tex file for each parameter constraint for input() in a paper')

#    parser.add_argument('--batchPath', help='directory containing the grid')
    parser.add_argument('--paramNameFile', default='clik_latex.paramnames', help=".paramnames file for overriding labels for parameters")

    args = parser.parse_args()

    params, labels, texs = margeParamTex(args.rootname, args.params, args.limit, args.paramNameFile)
    if args.tex_snippet_dir is not None:
        if not os.path.exists(args.tex_snippet_dir): os.makedirs(args.tex_snippet_dir)
        makeSnippetFiles(args.tex_snippet_dir , args.rootname, params, texs, tag='sig' + str(args.limit))
    else:
        for label, value in zip(labels, texs):
            print("{:<30} {:}".format(label, value))


