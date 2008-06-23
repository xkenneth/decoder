from ZEO import runzeo

def main(args=None):
    options = runzeo.ZEOOptions()
    options.realize(args)
    s = runzeo.ZEOServer(options)
    s.main()

if __name__ == '__main__':
    main()
    
    


