import luigi
import json
import sh
import glob
class Start(luigi.Task):
 
    def requires(self):
        return []
 
    def output(self):
        return luigi.LocalTarget("output.json")
 
    def run(self):
        data = {"start":"True"}
        with self.output().open('w') as f:
          json.dump(data,f)

class Runner(luigi.Task):
 
    def requires(self):
        return [DeleteUnneeded()]
 
    def output(self):
        return luigi.LocalTarget("output.json")
 
    def run(self):
        data = {"finished":"True"}
        with self.output().open('r') as f:
            existing = json.load(f)
        with self.output().open('w') as f:
            existing.update(data)
            json.dump(existing,f)



class PrepFileList(luigi.Task):
 
    def requires(self):
        return [Start()]
 
    def output(self):
        return luigi.LocalTarget("output.json")
 
    def run(self):
        files_list = glob.glob("*.mp3")
        data = {"download":"success","files_list":files_list}
        with self.output().open('r') as f:
            existing = json.load(f)
        with self.output().open('w') as f:
            existing.update(data)
            json.dump(existing,f)
          
class Converter(luigi.Task):
 
    def requires(self):
        return [PrepFileList()]
 
    def output(self):
        return luigi.LocalTarget("output.json")
    def convert_file(self,file_name):
        sh.python("py_split.py",file_name)
 
    def run(self):
        data = {"convert":"True"}
        with self.output().open('r') as f:
            existing = json.load(f)
            for song in existing['files_list']:
                self.convert_file(song)
        with self.output().open('w') as f:
            existing.update(data)
            json.dump(existing,f)

class DeleteUnneeded(luigi.Task): 
    def requires(self):
        return [Converter()]
 
    def output(self):
        return luigi.LocalTarget("output.json")
 
    def run(self):
        data = {"mp3_deleted":"True"}
        with self.output().open('r') as f:
            existing = json.load(f)
            for song in existing['files_list']:
                sh.rm(song)
        with self.output().open('w') as f:
            existing.update(data)
            json.dump(existing,f)

if __name__ == '__main__':
    luigi.run()
