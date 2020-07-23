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

package nl.cypherpunk.statelearner;

import net.automatalib.automata.transout.MealyMachine;
import net.automatalib.commons.util.mappings.MutableMapping;
import net.automatalib.words.Word;

import java.util.*;
import java.util.function.Consumer;

public class Utils {
	private static String CHARS = "0123456789ABCDEF";
	public static String bytesToHex(byte[] bytes) {
		StringBuffer hex = new StringBuffer();
		
		for(int i = 0; i < bytes.length; i++) {
			int n1 = (bytes[i] >> 4) & 0x0F;
			hex.append(CHARS.charAt(n1));
			int n2 = bytes[i] & 0x0F;
			hex.append(CHARS.charAt(n2));
		}
		
		return hex.toString();
	}
	
	public static byte[] hexToBytes(String hex) {
		//TODO Check if string contains only hex characters
		if(hex.length() % 2 != 0) hex = "0" + hex;
		
		byte[] bytes = new byte[hex.length() / 2];
		
		for(int i = 0; i < hex.length(); i = i + 2) {
			bytes[i/2] = Integer.decode("0x" + hex.substring(i, i + 2)).byteValue();
		}
			
		return bytes;
	}

	/**
	 * Utility method that allows to compute a state and transition cover simultaneously.
	 *
	 * @param automaton
	 *         the automaton for which the covers should be computed
	 * @param inputs
	 *         the set of input symbols allowed in the cover sequences
	 * @param states
	 *         the collection in which the state cover sequences will be stored
	 * @param transitions
	 *         the collection in which the transition cover sequences will be stored
	 *
	 * @see #randomTransitionCover(MealyMachine, Collection, LinkedHashSet, LinkedHashSet)
	 */

	public static void randomTransitionCover(MealyMachine<Integer, String, ?, String> automaton,
											  Collection<String> inputs,
											  LinkedHashSet<Word<String>> states,
											  LinkedHashSet<Word<String>> transitions) {

		Integer init = automaton.getInitialState();

		if (init == null) {
			return;
		}

		MutableMapping<Integer, Word<String>> reach = automaton.createStaticStateMapping();
		reach.put(init, Word.epsilon());

		Queue<Integer> bfsQueue = new ArrayDeque<>();
		bfsQueue.add(init);

		states.add(Word.epsilon());

		Integer curr;

		List<String> inputs_rnd = new ArrayList<>(inputs);
		while ((curr = bfsQueue.poll()) != null) {
			Word<String> as = reach.get(curr);
			assert as != null;

			Collections.shuffle(inputs_rnd);
			for (String in : inputs_rnd) {
				Integer succ = automaton.getSuccessor(curr, in);
				if (succ == null) {
					continue;
				}

				final Word<String> succAs = as.append(in);

				if (reach.get(succ) == null) {
					reach.put(succ, succAs);
					states.add(succAs);
					bfsQueue.add(succ);
				}
				transitions.add(succAs);
			}
		}
	}
}
