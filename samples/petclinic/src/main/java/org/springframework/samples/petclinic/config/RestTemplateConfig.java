package org.springframework.samples.petclinic.config;

import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.client.HttpComponentsClientHttpRequestFactory;
import org.springframework.web.client.RestTemplate;

@Configuration
public class RestTemplateConfig {

	@Bean
	public RestTemplate restTemplate() {
		CloseableHttpClient httpClient = HttpClients.custom()
			.setMaxConnTotal(100)
			.setMaxConnPerRoute(20)
			.build();

		HttpComponentsClientHttpRequestFactory requestFactory = new HttpComponentsClientHttpRequestFactory();
		requestFactory.setHttpClient(httpClient);
		requestFactory.setConnectTimeout(30000);
		requestFactory.setReadTimeout(30000);
		requestFactory.setConnectionRequestTimeout(30000);

		return new RestTemplate(requestFactory);
	}

}
