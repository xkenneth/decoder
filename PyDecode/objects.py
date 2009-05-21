class pydrill_object:
    def __ne__(self,other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

    def __eq__(self,other):
        """Keeps me from trying to see if objects equal each other!"""
        raise Exception('No!')

class tool_data(pydrill_object):
    def __init__(self,name,value=None,time_stamp=None,slowData=None):
        self.name = name
        self.fileKey = name
        self.value = value
        self.time_stamp = time_stamp
        self.slowData = slowData
		
    def __copy__(self):
        return tool_data(self.name,value=self.value,time_stamp=self.time_stamp,slowData=self.slowData)

    def __repr__(self):
        t = "ToolData: "
        try:
            t+= "N: " + str(self.name) + " "
        except AttributeError:
            pass
	
        try: 
            t+= "V: " + str(self.value) + " "
        except AttributeError:
            pass
        
        try: 
            t+= "T: " + str(self.time_stamp) + " "
        except AttributeError:
            pass
        
        try:
            t+= "SD: " + str(self.slowData) + " "
        except AttributeError:
            pass
        
        t +=  "End TD"
		
        return t

class symbol(pydrill_object):
    """This class represents a basic chirp"""
    def __init__(self,value=None,bars=None,time_stamp=None,pulses=None):

        self.value = value
        self.time_stamp = time_stamp
        
        self.bars = []
        if bars:
            self.bars.extend(bars) #take them if we've got them
            
        self.pulses = []
        if pulses:
            self.pulses.extend(pulses)
		 
        self.wide_mod_count = 2.0
        self.narrow_mod_count = 1.0
        
			 
    def __copy__(self):
        return symbol(value=self.value,bars=self.bars,time_stamp=self.time_stamp,pulses=self.pulses)
	 
	 #functions

# 	 def writeToXml(self,writer):
# 		 writer.startElement(u'Symbol')
# 		 if self.value is not None:
# 			 writer.simpleElement(u'Value',content=unicode(self.value))

# 		 if self.time_stamp!=None:
# 			 writer.simpleElement(u'TimeStamp',content=unicode(self.time_stamp))
		 
# 		 if self.bars is not None:
			 
		 

    def __len__(self):
        """Retruns the length of the symbol in modulus"""
        if self.bars is not None:
            modCount = 0
            for b in self.bars:
                if b.wide:
                    modCount += 2
                else:
                    modCount += 1
                    
            return modCount
			 
    def __val__(self):
        return self.value

    def symbolStart(self):
        """Returns the theoretical time that the symbol started based on the peaks present in the symbol."""
        rolling = 0.0
        for bar in self.bars:
            if bar.peak:
                if bar.wide:
                    rolling += self.wide_mod_count/2.0
                else:
                    rolling += self.narrow_mod_count/2.0
            else:
                if bar.wide:
                    rolling += self.wide_mod_count
                else:
                    rolling += self.narrow_mod_count

        return self.pulses[-1].time_stamp - mx.DateTime.DateTimeDeltaFrom(self.calcModulusTimeBase()*rolling)

    def firstPossiblePeakAfter(self,debug=False):
        """Returns the count in modulus from the last peak of a symbol until the time where a new peak can occur."""
        if debug:
            print

        myErr = ValueError('All elements required not defined.')
        if self.bars is None:
            raise myErr
        if self.pulses is None:
            raise myErr
        try:
            if len(self.pulses) == 0:
                raise myErr
        except TypeError:
            pass

		 #finding the last pulse in the symbol
        index = 0
        for b in range(len(self.bars)):
            if self.bars[b].peak:
                index = b
		 
        sum = 0
        if debug:
            print "Units after bar"
        if self.bars[index].wide:
            sum += 2.0/2.0
        else:
            sum += 1.0/2.0
			 
        for b in self.bars[index+1:]:
            if debug:
                print b
            if b.wide:
                sum += 2.0
            else:
                sum += 1.0

		 #since the quickest a pulse can occur is a narrow peak
		 #sum += 1.0/2.0
        narrow_start = sum + 1.0/2.0
        wide_start = sum + 2.0/2.0
        
        if debug:
            print sum

        symbol_start = sum

        return narrow_start,wide_start,symbol_start
				 
				 
			 
    def calcModulus(self):
        if self.bars is None: raise ValueError("Bars are not defined")
		 #print self.calcDeltas(cap=False)
		 #print self.numPeaks()
        return float(sum(self.calcDeltas(cap=False)))/float(self.numPeaks()-1)/2

    def calcModulusTimeBase(self):
        """Calculates the actual timebase based upon the bars and attached pulse times."""
        
        #if we don't have pulses or bars
        if len(self.pulses)==0 or len(self.bars) == 0:
            raise ValueError("Bars and/or Pulses are not defined")

        #if the number of pulses we have doesn't equal the number we should have
        if self.numPeaks() != len(self.pulses):
            raise ValueError("Symbol does not have as many pulses as peaks")
        
        #calculate the modulus from the beginning of the symbol to the end for each peak
        mods = []
        rolling = 0
        for b in self.bars:
            if b.wide:
                rolling += 2.0
            else:
                rolling += 1.0
				 
            if b.peak:
                if b.wide:
                    mods.append(rolling - 1.0)
                else:
                    mods.append(rolling - 0.5)

		 #calculate the differences between those modulus
        modsBetween = []
        
        last = None
        for m in mods:
            if last is not None:
                modsBetween.append(m-last)
            last = m

        #and calculate the difference between those deltas
        deltas = []
        last = None
        for d in self.pulses:
            if last is not None:
                deltas.append(float(d.time_stamp-last.time_stamp))
            last = d

        bases = []
		 
        #calculate the time base by delta/#mods
        for i in range(len(modsBetween)):
            bases.append(deltas[i]/modsBetween[i])
            
		 
        return sum(bases)/len(bases) #return the average of the mods

		 
		 
		 

	 
    def numPeaks(self):
        """Calculats the number of peaks in a symbol"""
        if self.bars is None:
            raise ValueError("Bars are not defined")
        count = 0
        for b in self.bars:
            if b.peak:
                count +=1
				 
        return count

    def calcDeltas(self,cap=True):
        from copy import copy

        if self.bars is None:
			 return []
		 
        modulus = 0.5

        last = None
        sum = 0.0
        deltas = []
		 
        newBars = []
        for b in self.bars:
            newBars.append(b)
		 
        if cap:
            newBars.append(bar(True))
            
        for b in newBars:
            if last is None:
                if b.peak:
                    last = b
                    if b.wide:
                        sum += modulus
                    else:
                        sum += modulus/2.0
            else:
                if b.peak:
                    last = b
                    if b.wide:
                        deltas.append(sum+modulus)
                        osum = modulus
                    else:
                        deltas.append(sum+modulus/2.0)
                        sum = modulus/2.0
					 
					 
				 
                else:
                    if b.wide:
                        sum += modulus*2.0
                    else:
                        sum += modulus

        return deltas
			 
    def __repr__(self):
        return '<Symbol(%d:%d) @ %s>' % (self.value,self.__len__(),self.time_stamp)

	 #called by the str(obj) function
class bar(pydrill_object):
    def __init__(self,peak,wide=False,time_stamp=None):
        self.peak,self.wide,self.time_stamp = peak,wide,time_stamp
        
    def __repr__(self):
        t = ''
        if self.wide:
            t += 'Wide '
        else:
            t += 'Narrow '

        if self.peak:
            t += 'Peak'
        else:
            t += 'Space'
            
        return t



    def __copy__(self):
        return bar(self.peak,wide=self.wide)

class sub_frame(pydrill_object):
	"""The class represents a sub-frame."""
	
     #CONSTRUCTOR
	def __init__(self,blocks=None,chirps=None,name=None,xml=None,time_stamp=None):
		"""blocks - a list of blocks"""
			 #switch for initialization

		self.blocks = []
		if blocks!=None:
			self.blocks.extend(blocks)
		self.name = name
		self.time_stamp = time_stamp

		if (xml!=None):
			self.loadFromXML(xml)

	def __copy__(self):
		from copy import copy
		newBlocks = []
		for b in self.blocks:
			newBlocks.append(copy(b))
		return sub_frame(blocks=newBlocks,name=self.name,time_stamp=self.time_stamp)

	def __len__(self):
		return len(self.blocks)

	def __repr__(self):
		t = "SubFrame\n"

		try:
			t += repr(self.name)
			t += "\n"
		except AttributeError:
			pass
		
		try:
			self.time_stamp
			t += "time: "
			t += str(self.time_stamp)
			t += "\n"

		except AttributeError:
			pass

		t += "Blocks\n"

		for i in self.blocks:
			t += repr(i) + "\n"
		
		t += "End Blocks\n"

		t += "End SubFrame"
		
		return t

	def sim(self):
		chirps = []
		for block in self.blocks:
			chirps.extend(block.sim())

		return chirps
	
	def decompose(self):

		#data = {}
		data = []
		for block in self.blocks:
			blockData = block.decompose()
			if blockData:
				data.append(blockData)
			
			
		for d in data:
			d.time_stamp = self.time_stamp
		return data
		
	def assimilate(self,other):
		for i in range(len(self.blocks)):
			try:
				self.blocks[i].name
			except AttributeError:
				self.blocks[i].name = other.blocks[i].name
		
		
class frame(pydrill_object):
    #basic initialization of the frame
    def __init__(self,header=None,subFrames=None,checkSum=None,xml=None,debug=False,time_stamp=None):
        """Basic constructor for the Frame Class"""        
	
	self.header = header
        
	self.subFrames = []

        if subFrames!=None:
            self.subFrames.extend(subFrames)

	self.checkSum = checkSum

	self.time_stamp = time_stamp
	
	self.debug = debug

    def __copy__(self):
	    from copy import copy

	    newSubFrames = []
            if self.subFrames != None:
                for sF in self.subFrames:
		    newSubFrames.append(copy(sF))
            if newSubFrames==[]:
                newSubFrames=None

                    
            
	    return Frame(header=copy(self.header),subFrames=newSubFrames,checkSum=copy(self.checkSum),time_stamp=self.time_stamp)

    def decompose(self):
	    data = []

	    finalData = []

	    dataDict = {}
            
	    for subFrame in self.subFrames:
		    newData = subFrame.decompose()
		    
		    data.extend(newData)

	    for d in data:
		    if len(d.value)==2:
			    finalData.append(d)
		    elif len(d.value)==1:
			    try:
				    dataDict[d.name].value = dataDict[d.name].value + d.value
				    dataDict[d.name].slowData = True
			    except KeyError:
				    dataDict[d.name] = d

	    for key in dataDict:
		    finalData.append(dataDict[key])

	    return finalData
			    
		    
		    
	    return data

    def sim(self,recursive=True):
	    data = [] #data to be returned

            if self.header is not None:
                try:
                    data.append(self.header.sim()) #create a chirp for the header
                except AttributeError:
                    #data.append(Chirp(value=-1))
                    data.append(Chirp(value=self.header))
                    
	    
            if self.subFrames!=None:
                for s in self.subFrames: #for all of the subFrames
		    try:
                        if recursive: #if recursive
                            data.extend(s.sim()) #return chirps for each subFrame
                        else:
                            data.append(s) #else just return the subFrame
		    except TypeError:
                        pass       

            if self.checkSum is not None:
                data.append(self.checkSum.sim()) #create a chirp for the checkSum
		
	    return data
			    
	    

    def value(self):
	    return self.header.value

        #ACCESSORS

    def __repr__(self):
	    #if not(self.isValid()):
	    #raise Exception('Frame is not valid')
	    
	    t =  "Frame "
	    
	    if self.time_stamp!=None:
		    t += 'TimeStamp: ' + str(self.time_stamp) + ' '
		
            if self.header!=None:
                t += "Header: " + str(self.header) + " "
	    
	    t += "SubFrames: "
	    for subFrame in self.subFrames:
		    t += str(subFrame) + " "

            if self.checkSum != None:
                t += "CheckSum: "
                t += str(self.checkSum)
                t += " End Frame"

	    return t

    def __str__(self):
	    return self.__repr__()
            

class chirp(pydrill_object):
	 """This class represents a basic chirp"""
	 #constructor
	 def __init__(self,value=None,deltas=None,xml=None,chirpLength=None,time_stamp=None,pulses=None,peaks=None,valleys=None):
		 """Takes the place of a default constructor. Arguments must either be the value of the chirp and the associated deltas, or an 4Suite XML Element"""

		 self.value = value
		 self.chirpLength = chirpLength
		 self.time_stamp = time_stamp
		 self.pulses = pulses
		 self.deltas = deltas
		 self.peaks = None
		 self.valleys = None
		 try:
			 if peaks is not None:
                             self.peaks = []
                             self.peaks.extend(peaks)

		 except AttributeError:
			 pass

		 try:
			 if valleys is not None:
                             self.valleys = []
                             self.valleys.extend(peaks)
		 except AttributeError:
			 pass
		 
		 if deltas is not None:
                     self.deltas = []
                     self.deltas.extend(deltas) #take them if we've got them
			 
		 if pulses is not None:
                     self.pulses = []
                     self.pulses.extend(pulses)
		 
	 def __copy__(self):
		 return Chirp(value=self.value,deltas=self.deltas,chirpLength=self.chirpLength,time_stamp=self.time_stamp,pulses=self.pulses)
	 
	 #called by the repr(obj) function
	 def __repr__(self):
		 t =  "Chirp"

		 if self.chirpLength!=None:
			 t += " len(cl): " + unicode(self.chirpLength)
			 t += ' '

		 if self.deltas!=None and len(self.deltas)>0:
			 t += " len(d): " + str(len(self.deltas))
			 t += ' '
		 		
		 if self.time_stamp!=None:
			 t += "time: " + str(self.time_stamp)

		 if self.value!=None:
			 t += " val: " + unicode(self.value)
			 t += ' '

		 if self.pulses != None:
			 t += " " + str(len(self.pulses)) + " Pulses Attached "

		 if self.peaks is not None:
			 t += " Peaks: "
			 for p in self.peaks: t += " " + p + " "

		 if self.valleys is not None:
			 t += " Valleys: "
			 for v in self.valleys: t += " " + v + " "

		 return t

class element(pydrill_object):
	#BASIC CONSTRUCTOR
	"""This class represents a particular element of a frame, such as a header,checkSum,etc"""
	def __init__(self,chirpLength=None,identifier=None,value=None,xml=None,time_stamp=None):
		"""Constructor for the class"""
		
		self.chirpLength = chirpLength
		self.identifier = identifier
		self.value = value
		self.time_stamp = time_stamp

		#try and load from the XML tag
		if (xml!=None):
			self.loadFromXML(xml)

	def __copy__(self):
		return element(chirpLength=self.chirpLength,identifier=self.identifier,value=self.value,time_stamp=self.time_stamp)

	def loadFromChirp(self,chirp,identifier=None):
		self.chirpLength = len(chirp)
		self.identifier = identifier
		self.value = chirp.value
		try:
			self.time_stamp = chirp.time_stamp
		except AttributeError:
			pass

	def doesForceValue(self):
		try:
			self.value
			return True
		except:
			raise ValueError('Not Initialized')

	def __repr__(self):

		t = "Frame Element "
		if self.chirpLength!=None:
			t += "Chirp Length: " + repr(self.chirpLength)

		if self.identifier!=None:
			t += " Identifier: " + repr(self.identifier)

		if self.value!=None:
			t += " Value: " + repr(self.value)

		return t

	def sim(self):
		try:
			value = self.value
		except AttributeError:
			value = None
			
                return chirp(value=value,chirpLength=self.chirpLength)

class block(pydrill_object):
	"""Blocks are used to represent sections within a frame."""
	def __init__(self,name=None,value=None,time_stamp=None,symbol_length=None):
		"""chirpLengths: a list of integers representing the lengths of the chirps in the frame"""
		
		self.name = name
		self.time_stamp = time_stamp
                
		self.value = value
                #the number of symbols long the block is
		self.symbol_length = symbol_length 

        def __repr__(self):
            return '<Block(%s) value:%s len:%s @ %s>' % (self.name,self.value,self.symbol_length,self.time_stamp)

        def __len__(self):
		"""Return the length of the block in symbols"""
		return self.symbol_length

	def __copy__(self):
		return Block(chirpLengths=self.chirpLengths,name=self.name,time_stamp=self.time_stamp,symbol_length=self.symbol_length)

	def decompose(self):
            if self.name != None:
                slowData=False
                return tool_data(self.name,self.value,self.time_stamp,slowData)
            
	def sim(self):
            chirps = []
            for i in self.chirpLengths:
                chirps.append(chirp(chirpLength=i))

            if self.symbol_length is not None:
                for s in range(self.symbol_length):
                    chirps.append(chirp())

            return chirps

class symbol_frame(pydrill_object):
    
    def __init__(self,
                 identifier=None,
                 blocks=None,
                 symbols=None,
                 ):
        
        """Initialize a frame
        identifier - a symbol that acts as an identifier for the frame
        blocks - the individual data blocks
        """
        
        self.identifier = identifier
        self.blocks = blocks
        self.symbols = symbols
        
    def __copy__(self):
        """Returns a fresh copy of the object"""
        return symbol_frame(identifier=self.identifier,
                           blocks=self.blocks,
                           symbols=self.symbols,
                           )
                           
    def sim(self):
        """Decompose a frame into it's smaller elements"""
        
        data = [self.identifier]
        #for all the blocks
        for block in self.blocks:
            data.extend(block.sim())

        return data

    def decompose(self):
        """Decompose a completed frame into tooldata"""
        data = {}
        
        count = 0
        for block in self.blocks:
            for i in range(len(block)):
                try:
                    #data[block.name] = ( data[block.name] * 100 ) + self.symbols[count].value
                    data[block.name].value = ( data[block.name].value * 100 ) + self.symbols[count].value
                except KeyError:
                    data[block.name] = tool_data(block.name,value=self.symbols[count].value,time_stamp=self.symbols[count].time_stamp)
                count += 1

        #print data

        found_tool_data = []

        for d in data:
            found_tool_data.append(data[d])

        return found_tool_data


    def __len__(self):
        """Return the length of the frame in symbols including the frame ID but not the sync."""
        count = 1
        for block in self.blocks:
            count += len(block)

        return count
