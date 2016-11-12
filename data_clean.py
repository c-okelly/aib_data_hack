# Author Conor O'Kelly
import numpy as np
import pandas as pd


def load_data():

    data = pd.read_csv("back_up.csv")

    # print(data.head())
    # Remove nan values and repacle with ?

    # Drop headers
    data = data.drop(0, axis=0) #remove the row at index 0, only headers
    # Cleaning Format of features
    # Remove sqe mt on floor
    data['GroundFloorArea'] = data['GroundFloorArea'].map(lambda x: x[:-6] if type(x)==str else "")
    # Formate year
    data['Year'] = data['Year'].map(lambda x: x[1:-2])
    # Clean main space energy
    data['MainSpaceEnergy'] = data['MainSpaceEnergy'].map(lambda x: str(x))
    data['MainSpaceEnergy'] = data['MainSpaceEnergy'].map(lambda x: x.replace('"',''))
    data['MainSpaceEnergy'] = data['MainSpaceEnergy'].map(lambda x: x.replace('-',''))
    data['MainSpaceEnergy'] = data['MainSpaceEnergy'].map(lambda x: float(x))
    def convert(x):
        try:
            y = float((x[:-1]))/100
            return y
        except:
            print(x)
            return x

    # Format column with percentage
    data["PercLivingArea"] = data["PercLivingArea"].map(lambda x: convert(x))

    # Convert to int
    # data.convert_objects(convert_numeric=True)
    data["GroundFloorArea"] = data["GroundFloorArea"].apply(pd.to_numeric)
    # Remove columns that have less then 90% for all values
    print(data.dtypes)
    # Remove na values
    # data = data.fillna("?")

    data = data.head(n=30)

    # Save out put as csv files
    # data.to_csv("Numeric.csv") 
    pandas2arff(data,"train.arff")

def pandas2arff(df,filename,wekaname = "pandasdata",cleanstringdata=True,cleannan=True):
    """
    converts the pandas dataframe to a weka compatible file
    df: dataframe in pandas format
    filename: the filename you want the weka compatible file to be in
    wekaname: the name you want to give to the weka dataset (this will be visible to you when you open it in Weka)
    cleanstringdata: clean up data which may have spaces and replace with "_", special characters etc which seem to annoy Weka. 
                     To suppress this, set this to False
    cleannan: replaces all nan values with "?" which is Weka's standard for missing values. 
              To suppress this, set this to False
    """
    import re
    
    def cleanstring(s):
        if s!="?":
            return re.sub('[^A-Za-z0-9]+', "_", str(s))
        else:
            return "?"
            
    dfcopy = df #all cleaning operations get done on this copy

    
    if cleannan!=False:
        dfcopy = dfcopy.fillna(-999999999) #this is so that we can swap this out for "?"
        #this makes sure that certain numerical columns with missing values don't get stuck with "object" type
 
    f = open(filename,"w")
    arffList = []
    arffList.append("@relation " + wekaname + "\n")
    #look at each column's dtype. If it's an "object", make it "nominal" under Weka for now (can be changed in source for dates.. etc)
    for i in range(df.shape[1]):
        if dfcopy.dtypes[i]=='O' or (df.columns[i] in ["Class","CLASS","class"]):
            if cleannan!=False:
                dfcopy.iloc[:,i] = dfcopy.iloc[:,i].replace(to_replace=-999999999, value="?")
            if cleanstringdata!=False:
                dfcopy.iloc[:,i] = dfcopy.iloc[:,i].apply(cleanstring)
            _uniqueNominalVals = [str(_i) for _i in np.unique(dfcopy.iloc[:,i])]
            _uniqueNominalVals = ",".join(_uniqueNominalVals)
            _uniqueNominalVals = _uniqueNominalVals.replace("[","")
            _uniqueNominalVals = _uniqueNominalVals.replace("]","")
            _uniqueValuesString = "{" + _uniqueNominalVals +"}" 
            arffList.append("@attribute " + df.columns[i] + _uniqueValuesString + "\n")
        else:
            arffList.append("@attribute " + df.columns[i] + " real\n") 
            #even if it is an integer, let's just deal with it as a real number for now
    arffList.append("@data\n")           
    for i in range(dfcopy.shape[0]):#instances
        _instanceString = ""
        for j in range(df.shape[1]):#features
                if dfcopy.dtypes[j]=='O':
                    _instanceString+="\"" + str(dfcopy.iloc[i,j]) + "\""
                else:
                    _instanceString+=str(dfcopy.iloc[i,j])
                if j!=dfcopy.shape[1]-1:#if it's not the last feature, add a comma
                    _instanceString+=","
        _instanceString+="\n"
        if cleannan!=False:
            _instanceString = _instanceString.replace("-999999999.0","?") #for numeric missing values
            _instanceString = _instanceString.replace("\"?\"","?") #for categorical missing values
        arffList.append(_instanceString)
    f.writelines(arffList)
    f.close()
    del dfcopy
    return True



if (__name__ == "__main__"):

    print('Start')
    load_data()
    print("Finish")

