package mapreduceproject;

import java.io.IOException;
import java.util.*;
import org.apache.commons.lang3.StringUtils;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.ArrayWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class SocialNetwork {
	public static class MyMapper
    extends Mapper<Object, Text, IntWritable, IntWritable>{

 private final static IntWritable one = new IntWritable(1);
 

 public void map(Object key, Text value, Context context
                 ) throws IOException, InterruptedException {
   StringTokenizer itr = new StringTokenizer(value.toString());
   
   itr.nextToken(); //ignore first token
   String[] friends = itr.nextToken().split(",",0);
   for(String friend1: friends){
     for (String friend2: friends){
         
         context.write(new IntWritable(Integer.parseInt(friend1)),new IntWritable(Integer.parseInt(friend2)));
     }
   }
   
   
 }
}

public static class MyReducer
    extends Reducer<IntWritable,IntWritable,IntWritable,Text> {
	Text result=new Text();

 public void reduce(IntWritable key, Iterable<IntWritable> values,
                    Context context
                    ) throws IOException, InterruptedException {
   Hashtable<Integer,Integer> table=new Hashtable<Integer,Integer>();
   for (IntWritable val : values) {
     int friend = val.get();
     if(table.contains(friend)){
         table.put(friend,table.get(friend)+1);
     }
     else{
         table.put(friend,1);
     }
   }
   ArrayList<Integer> list=new ArrayList<>(table.values());
   Collections.sort(list,Collections.reverseOrder());
 
   String resultString=StringUtils.join(',',list.subList(0,4));
   result.set(resultString);
   context.write(key, result);
 }
}

public static void main(String[] args) throws Exception {
 Configuration conf = new Configuration();
 Job job = Job.getInstance(conf, "social network");
 job.setJarByClass(SocialNetwork.class);
 job.setMapperClass(MyMapper.class);
 job.setReducerClass(MyReducer.class);
 job.setOutputKeyClass(IntWritable.class);
 job.setOutputValueClass(Text.class);
 FileInputFormat.addInputPath(job, new Path(args[0]));
 FileOutputFormat.setOutputPath(job, new Path(args[1]));
 System.exit(job.waitForCompletion(true) ? 0 : 1);
}
}
