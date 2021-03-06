#! /usr/bin/env python

import gcat_workflow_cloud.abstract_task as abstract_task

class Task(abstract_task.Abstract_task):
    CONF_SECTION = "gatk_haplotypecaller_parabricks_compatible"
    TASK_NAME = CONF_SECTION

    def __init__(self, task_dir, sample_conf, param_conf, run_conf):

        super(Task, self).__init__(
            "compat-haplotypecaller.sh",
            param_conf.get(self.CONF_SECTION, "image"),
            param_conf.get(self.CONF_SECTION, "resource"),
            run_conf.output_dir + "/logging"
        )
        
        self.task_file = self.task_file_generation(task_dir, sample_conf, param_conf, run_conf)

    def task_file_generation(self, task_dir, sample_conf, param_conf, run_conf):

        task_file = "{}/{}-tasks-{}.tsv".format(task_dir, self.TASK_NAME, run_conf.project_name)
        with open(task_file, 'w') as hout:
            
            hout.write(
                '\t'.join([
                    "--input-recursive REFERENCE_DIR",
                    "--env REFERENCE_FASTA",
                    "--input INTERVAL_AUTOSOME",
                    "--input INTERVAL_PAR",
                    "--input INTERVAL_CHRX",
                    "--input INTERVAL_CHRY",
                    "--input INPUT_CRAM",
                    "--input INPUT_CRAI",
                    "--output-recursive OUTPUT_DIR",
                    "--env SAMPLE",
                    "--env GATK_JAR",
                ]) + "\n"
            )
            for sample in sample_conf.haplotype_call:
                hout.write(
                    '\t'.join([
                        param_conf.get(self.CONF_SECTION, "reference_dir"),
                        param_conf.get(self.CONF_SECTION, "reference_file"),
                        param_conf.get(self.CONF_SECTION, "interval_file_autosome"),
                        param_conf.get(self.CONF_SECTION, "interval_file_par"),
                        param_conf.get(self.CONF_SECTION, "interval_file_chrx"),
                        param_conf.get(self.CONF_SECTION, "interval_file_chry"),
                        "%s/cram/%s/%s.markdup.cram" % (run_conf.output_dir, sample, sample),
                        "%s/cram/%s/%s.markdup.cram.crai" % (run_conf.output_dir, sample, sample),
                        "%s/haplotypecaller/%s" % (run_conf.output_dir, sample),
                        "%s" % (sample),
                        param_conf.get(self.CONF_SECTION, "gatk_jar"),
                    ]) + "\n"
                )

        return task_file
