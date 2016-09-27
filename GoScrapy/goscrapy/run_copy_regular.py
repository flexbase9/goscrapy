from model.regular import Regular
import sys
if len(sys.argv)==3:
    from_project=sys.argv[1]
    to_project=sys.argv[2]
    if len(to_project) == 0:
        from_project=sys.argv[2]
        to_project=sys.argv[1]
    print sys.argv
    print 'Start Copy...'
    print 'From: %s ======>>>> To: %s' % (from_project,to_project)
    Regular.copy_project_to(from_project, to_project)