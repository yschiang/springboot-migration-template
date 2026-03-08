package org.springframework.samples.petclinic.config;

import org.springframework.batch.core.Job;
import org.springframework.batch.core.Step;
import org.springframework.batch.core.configuration.annotation.EnableBatchProcessing;
import org.springframework.batch.core.configuration.annotation.JobBuilderFactory;
import org.springframework.batch.core.configuration.annotation.StepBuilderFactory;
import org.springframework.batch.repeat.RepeatStatus;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
@EnableBatchProcessing
public class BatchConfig {

	private final JobBuilderFactory jobBuilderFactory;

	private final StepBuilderFactory stepBuilderFactory;

	public BatchConfig(JobBuilderFactory jobBuilderFactory, StepBuilderFactory stepBuilderFactory) {
		this.jobBuilderFactory = jobBuilderFactory;
		this.stepBuilderFactory = stepBuilderFactory;
	}

	@Bean
	public Job vetDataExportJob() {
		return jobBuilderFactory.get("vetDataExportJob")
			.start(exportStep())
			.build();
	}

	@Bean
	public Job visitReminderJob() {
		return jobBuilderFactory.get("visitReminderJob")
			.start(reminderStep())
			.build();
	}

	@Bean
	public Step exportStep() {
		return stepBuilderFactory.get("exportStep")
			.tasklet((contribution, chunkContext) -> {
				// export vet data
				return RepeatStatus.FINISHED;
			}).build();
	}

	@Bean
	public Step reminderStep() {
		return stepBuilderFactory.get("reminderStep")
			.tasklet((contribution, chunkContext) -> {
				// send visit reminders
				return RepeatStatus.FINISHED;
			}).build();
	}

}
