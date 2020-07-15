/*
 *  Copyright (c) 2016 Joeri de Ruiter
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 */

package nl.cypherpunk.statelearner.tls;

import java.util.Arrays;
import java.util.logging.Level;

import de.learnlib.logging.LearnLogger;
import net.automatalib.words.impl.SimpleAlphabet;
import nl.cypherpunk.statelearner.Learner;
import nl.cypherpunk.statelearner.StateLearnerSUL;

/**
 * @author Joeri de Ruiter (joeri@cs.ru.nl)
 * @author Diego Damasceno (damasceno.diego@gmail.com)
 */
public class TLSSUL implements StateLearnerSUL<String, String> {
	SimpleAlphabet<String> alphabet;
	TLSTestService tls;
	LearnLogger logger;
	
	public TLSSUL(TLSConfig config) throws Exception {
		logger = LearnLogger.getLogger(TLSSUL.class.getSimpleName());
		alphabet = new SimpleAlphabet<>(Arrays.asList(config.alphabet.split(" ")));
		logger.log(Level.INFO, "Using the alphabet: " + alphabet.toString());

		tls = new TLSTestService();
		
		tls.setTarget(config.target);
		logger.log(Level.INFO, "Target: " + config.target);
		tls.setHost(config.host);
		logger.log(Level.INFO, "Host: " + config.host);
		tls.setPort(config.port);
		logger.log(Level.INFO, "Port: " + config.port);
		tls.setCommand(config.cmd);
		logger.log(Level.INFO, "Cmd: " + config.cmd);
		tls.setRequireRestart(config.restart);
		logger.log(Level.INFO, "Restart: " + config.restart);
		tls.setReceiveMessagesTimeout(config.timeout);
		logger.log(Level.INFO, "Timeout: " + config.timeout);
		tls.setKeystore(config.keystore_filename, config.keystore_password);
		logger.log(Level.INFO, "Filename: " + config.keystore_filename);
		logger.log(Level.INFO, "Password: " + config.keystore_password);
		tls.setConsoleOutput(config.console_output);
		logger.log(Level.INFO, "Console: " + config.console_output);

		if(config.version.equals("tls10")) {
			tls.useTLS10();
			logger.log(Level.INFO, "Version: " + "tls10");
		}
		else {
			tls.useTLS12();
			logger.log(Level.INFO, "Version: " + "tls12");
		}
		
		tls.start();
	}
	
	public SimpleAlphabet<String> getAlphabet() {
		return alphabet;
	}	

	public boolean canFork() {
		return false;
	}
	
	@Override
	public String step(String symbol) {
		String result = null;
		try {
			long startTime = System.nanoTime();
			result = tls.processSymbol(symbol);
			long stopTime = System.nanoTime();
			logger.log(Level.INFO, "Step TimedIO: " +"["+(stopTime-startTime)+"]\t"+ symbol+"\t/\t"+result);
		} catch (Exception e) {
			e.printStackTrace();
		}
		return result;
	}

	@Override
	public void pre() {
		try {
			long startTime = System.nanoTime();
			tls.reset();
			long stopTime = System.nanoTime();
			logger.log(Level.INFO, "Step Reset: " +"["+(stopTime-startTime)+"]");
		} catch (Exception e) {
			e.printStackTrace();
			throw new RuntimeException(e);
		}	
	}

	@Override
	public void post() {
	}
	
}
